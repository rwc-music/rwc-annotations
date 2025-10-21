# RWC 2.0 Annotations

RWC 2.0 is a re-release of the original RWC dataset under a Creative Commons license (Goto et al., 2002). This repository collects curated annotations for RWC 2.0 that satisfy the following requirements:

- Annotation filenames are consistent with the released audio files (e.g., matching base names).
- Annotation formats are simple, easy to parse, and well documented — units are explicit (for example, beat times given in seconds).
- Each annotation type includes a README describing the format: column meanings, units, example files, and any conversion notes.

Contributions are welcome. To propose fixes or additions, please open an issue describing the change or submit a pull request with your proposed updates.

## Repository Structure

### 01_annotations_preprocessed



### 02_annotations_derived

There is certainly no file format for all possible applications.
Some applications require specific file format, e.g, it is easier to use JSON files in web applications.
In `01_annotations_preprocessed`, we decided to use very simple file formats as we think that converting to a more complex
format from this will always be possible through suitable scripts.
In `02_annotations_derived`, we collect conversion scripts and the converted annotations in various formats.

## Bibliography

We provide a list of central publications on the legacy of the RWC dataset.
However, annotations for this dataset may have been presented in other publications.
For the sake of reproducibility, please make sure to cite the original publications.

```bibtex
@inproceedings{GotoHNO02_RWC_ISMIR,
  address = {Paris, France},
  author = {Masataka Goto and Hiroki Hashiguchi and Takuichi Nishimura and Ryuichi Oka},
  booktitle = {Proceedings of the International Society for Music Information Retrieval Conference ({ISMIR})},
  pages = {287--288},
  title = {{RWC} Music Database: Popular, Classical and Jazz Music Databases},
  year = {2002}
}
```

```bibtex
@inproceedings{GotoHNO03_RWCGenre_ISMIR,
  author    = {Masataka Goto and Hiroki Hashiguchi and Takuichi Nishimura and Ryuichi Oka},
  title     = {{RWC} Music Database: Music genre database and musical instrument sound database},
  booktitle = {Proceedings of the International Society for Music Information Retrieval Conference ({ISMIR})},
  address   = {Baltimore, Maryland, USA},
  year      = {2003},
  pages     = {229--230},
}
```

```bibtex
@inproceedings{Goto06_AnnotationsAIST_ISMIR,
  author    = {Masataka Goto},
  title     = {{AIST} Annotation for the {RWC} Music Database},
  booktitle = {Proceedings of the International Society for Music Information Retrieval Conference ({ISMIR})},
  year      = {2006},
  pages     = {359--360},
}
```

## License

This project is licensed under the **CC BY-NC 4.0** - see the [LICENSE](./LICENSE) file for details.

## Acknowledgements

The creation of the original RWC was by Masataka Goto in 2001. All credits for the creation belong to him.
He was supported by experts in the field who played an important role to make the RWC reality.

For the release of RWC 2.0, Meinard Müller and Stefan Balke were supported by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation)
under grant number 500643750 (MU 2686/15-1). The [International Audio Laboratories Erlangen](https://audiolabs-erlangen.de) are a joint
institution of the [Friedrich-Alexander-Universität Erlangen-Nürnberg (FAU)](https://www.fau.eu) and [Fraunhofer Institute for Integrated Circuits IIS](https://www.iis.fraunhofer.de/en.html).
