# Change Log
Arquivo para documentação das mudanças realizadas ao longo do projeto. O formato desse arquivo é baseado no [Keep a Changelog](http://keepachangelog.com/)
e o presente projeto adota o [Semantic Versioning](http://semver.org/).

## [0.4.0] - 2021-11-17
- [COT-399](https://ecoanalytics.atlassian.net/browse/COT-399)
### Adicionado
- Sobrescrito a função `image_downloaded` do objeto `ImagesPipeline` para garantir a persistência de apenas imagens que ainda não estão salvas no storage.

## [0.3.1] - 2021-11-14
### [COT-371](https://ecoanalytics.atlassian.net/browse/COT-371)
#### Alterado
- Alterado o atributo `sku_alt` para ser uma lista ao invés de None.

## [0.3.0] - 2021-11-13
### [COT-367](https://ecoanalytics.atlassian.net/browse/COT-367)
#### Adicionado
- Adicionado `ItemCountMonitor` a suite de monitores.
- Adicionado `NikeFemaleSpider`, `NikeMaleSpider`.
#### Removido
- Removido persistência de arquivos 800x600.
- Removido `SkuValidationMonitor`
## [0.2.0] - 2021-10-09
### [COT-201](https://ecoanalytics.atlassian.net/browse/COT-201)
#### Alterado
- Alterado o parâmetro `IMAGES_THUMBS` para coletar imagens de 400x400.
#### Adicionado
- Adicionado a feature `reference_first_image` ao objeto `KingsItem`.