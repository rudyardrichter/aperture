use pyo3::{exceptions::PyValueError, prelude::*, types::PyType};
use regex::Regex;
use std::fs::read_to_string;

/// Store a dictionary of words as a single linebreak-separated string to search through using
/// regexes.
#[pyclass(
    module = "match_engine",
    name = "MatchEngine",
    text_signature = "(str)",
    unsendable
)]
pub struct MatchEngine {
    words: String,
}

impl MatchEngine {
    #[allow(dead_code)]
    fn rs_from_file(filepath: &str) -> Result<Self, std::io::Error> {
        Ok(Self::new(read_to_string(filepath)?))
    }
}

#[pymethods]
impl MatchEngine {
    #[new]
    fn new(words: String) -> Self {
        MatchEngine { words }
    }

    /// Initialize the engine with a dictionary file. The file must be formatted as individual
    /// words separated by linebreaks.
    #[classmethod]
    pub fn from_file(_cls: &PyType, filepath: &str) -> PyResult<Self> {
        // cls.call_method1("__init__", (read_to_string(filepath)?,))
        Ok(Self {
            words: read_to_string(filepath)?,
        })
    }

    /// Return a list of words that match a pattern.
    pub fn matches(&self, pattern: &str) -> PyResult<Vec<&str>> {
        Ok(Regex::new(&format!(r"(?m)^{}$", pattern))
            .map_err(|e| PyValueError::new_err(format!("invalid regex: {:?}", e)))?
            .find_iter(&self.words)
            .map(|match_| match_.into())
            .collect())
    }
}

#[pymodule]
fn match_engine(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<MatchEngine>()?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use tempfile::NamedTempFile;

    use super::*;
    use std::io::prelude::Write;

    #[test]
    fn test_engine_matches() {
        let mut file = NamedTempFile::new().unwrap();
        const CONTENTS: &str = "foo\nfoooo\nbar\nbaz";
        write!(file, "{}", CONTENTS).unwrap();
        let engine = MatchEngine::rs_from_file(file.path().to_str().unwrap()).unwrap();
        assert_eq!(engine.words, CONTENTS.to_string());
        assert_eq!(engine.matches("foo").unwrap(), vec!["foo"]);
        assert_eq!(engine.matches("fo*").unwrap(), vec!["foo", "foooo"]);
        assert_eq!(engine.matches("ba.").unwrap(), vec!["bar", "baz"]);
        assert_eq!(engine.matches("b.*").unwrap(), vec!["bar", "baz"]);
    }
}
