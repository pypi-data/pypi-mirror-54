from .GraphicRecord import GraphicRecord
from .CircularGraphicRecord import CircularGraphicRecord
from .GraphicFeature import GraphicFeature
from Bio import SeqIO


class BiopythonTranslator:
    """A translator from SeqRecords to dna_features_viewer GraphicRecord.

    This can be subclassed to create custom "themes" (see the example
    ``custom_biopython_translator.py`` in the docs).

    This class is meant to be customized by subclassing and changing the
    methods (``compute_feature_label``, etc.) and/or the attributes
    (``default_feature_color`` etc).

    Attributes
    ----------

    default_feature_color = "#7245dc"
    graphic_record_parameters
      Dictionnary containing keyword arguments that will be passed to the
      (Circular)GraphicRecord constructor

    ignored_features_types
      A list or tuple of strings indicating all the feature types that should
      always be ignored (i.e. not included in the graphic record) by the
      translator

    max_label_length
      Number of characters above which the labels will be printed cut and
      ended with an ellipsis "…". This is to prevent extra-long labels from
      polluting the whole plots.

    max_line_length
      Feature labels with a number of characters above this number will be
      wrapped on 2 or more lines.

    label_fields
      This list of strings provides the order in which the different
      attributes of a Genbank feature will be considered, when automatically
      determining the feature label. For instance if the list is
      ["label", "source", "locus_tag"] and a feature has no label but has a
      "source", the "source" will be displayed in the plots.

    Parameters
    ----------

    features_filters
      List of filters (some_biopython_feature) => True/False.
      Only features passing all the filters are kept.
      This only works if you haven't redefined ``compute_filtered_features``

    features_properties
      A function (feature)=> properties_dict

    """

    default_feature_color = "#7245dc"
    graphic_record_parameters = {}
    ignored_features_types = ()
    label_fields = ["label", "source", "locus_tag", "note", "gene", "product"]

    def __init__(self, features_filters=(), features_properties=None):
        self.features_filters = features_filters
        self.features_properties = features_properties

    def compute_feature_color(self, feature):
        """Compute a color for this feature.

        If the feature has a ``color`` qualifier it will be used. Otherwise,
        the classe's ``default_feature_color`` is used.

        To change the behaviour, create a subclass of ``BiopythonTranslator``
        and overwrite this method.
        """
        if "color" in feature.qualifiers:
            color = feature.qualifiers["color"]
            if isinstance(color[0], str):
                return "".join(feature.qualifiers["color"])
            else:
                return color
        else:
            return self.default_feature_color

    def compute_feature_fontdict(self, feature):
        """Compute a font dict for this feature.
        """
        return None

    def compute_feature_box_linewidth(self, feature):
        """Compute a box_linewidth for this feature.
        """
        return 1

    def compute_feature_box_color(self, feature):
        """Compute a box_color for this feature.
        """
        return "auto"

    def compute_filtered_features(self, features):
        return [
            f
            for f in features
            if all([fl(f) for fl in self.features_filters])
            and f.type not in self.ignored_features_types
        ]

    def compute_feature_label(self, feature):
        label = feature.type
        for key in self.label_fields:
            if key in feature.qualifiers and len(feature.qualifiers[key]):
                label = feature.qualifiers[key]
                break
        if isinstance(label, list):
            label = "|".join(label)
        return label

    def compute_feature_html(self, feature):
        """Gets the 'label' of the feature."""
        return self.compute_feature_label(feature)

    def translate_feature(self, feature):
        """Translate a Biopython feature into a Dna Features Viewer feature."""
        properties = dict(
            label=self.compute_feature_label(feature),
            color=self.compute_feature_color(feature),
            html=self.compute_feature_html(feature),
            fontdict=self.compute_feature_fontdict(feature),
            box_linewidth=self.compute_feature_box_linewidth(feature),
            box_color=self.compute_feature_box_color(feature),
        )
        if self.features_properties is not None:
            other_properties = self.features_properties(feature)

        else:
            other_properties = {}
        properties.update(other_properties)

        return GraphicFeature(
            start=feature.location.start,
            end=feature.location.end,
            strand=feature.location.strand,
            **properties
        )

    def translate_record(self, record, record_class=None):
        """Create a new GraphicRecord from a BioPython Record object.

        Parameters
        ----------

        record
          A BioPython Record object or the path to a Genbank file.

        record_class
          The graphic record class to use, e.g. GraphicRecord (default) or
          CircularGraphicRecord. Strings 'circular' and 'linear' can also be
          provided.
        """
        classes = {
            "linear": GraphicRecord,
            "circular": CircularGraphicRecord,
            None: GraphicRecord,
        }
        if record_class in classes:
            record_class = classes[record_class]

        if isinstance(record, str):
            record = SeqIO.read(record, "genbank")
        filtered_features = self.compute_filtered_features(record.features)
        return record_class(
            sequence_length=len(record),
            sequence=str(record.seq),
            features=[
                self.translate_feature(feature)
                for feature in filtered_features
                if feature.location is not None
            ],
            **self.graphic_record_parameters
        )
