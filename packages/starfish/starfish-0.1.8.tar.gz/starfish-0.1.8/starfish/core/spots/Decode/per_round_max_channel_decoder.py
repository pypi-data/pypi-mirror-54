from starfish.core.codebook.codebook import Codebook
from starfish.core.intensity_table.decoded_intensity_table import DecodedIntensityTable
from starfish.core.intensity_table.intensity_table import IntensityTable
from ._base import DecodeAlgorithm


class PerRoundMaxChannel(DecodeAlgorithm):
    """
    Decode spots by selecting the max-valued channel in each sequencing round.

    Note that this assumes that the codebook contains only one "on" channel per sequencing round,
    a common pattern in experiments that assign one fluorophore to each DNA nucleotide and
    read DNA sequentially. It is also a characteristic of single-molecule FISH and RNAscope
    codebooks.

    Parameters
    ----------
    codebook : Codebook
        Contains codes to decode IntensityTable

    """

    def __init__(self, codebook: Codebook):
        self.codebook = codebook

    def run(self, intensities: IntensityTable, *args) -> DecodedIntensityTable:
        """Decode spots by selecting the max-valued channel in each sequencing round

        Parameters
        ----------
        intensities : IntensityTable
            IntensityTable to be decoded

        Returns
        -------
        IntensityTable :
            IntensityTable decoded and appended with Features.TARGET and Features.QUALITY values.

        """
        return self.codebook.decode_per_round_max(intensities)
