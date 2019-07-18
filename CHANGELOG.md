# UK Polar Data Centre (UK PDC) Metadata Record Generator

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

* controlled titles in responsible parties (ISNI and ORCID) following 
* OnlineResources were incorrectly placed in ResponsibleParties, rather than inside a ContentInfo element [#33]
  [uk-pdc/metadata-infrastructure/metadata-standards#92]
* adding better URL for netCDF MIME type
* adding missing change log header

## [0.1.0] 2019-06-28

### Added

* Initial version with support for ISO 19115

