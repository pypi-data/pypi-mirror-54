Feature: `rxdata.field(evolves=[...])` applies pipelines on init and/or attribute set
    `rxdata.field` results will apply pipeline from attribute `evolve`
    Rule: `field(evolves=[...])` pipeline executed upon init and on field `setattr`
      @rxdataobject.evolves.init.defaults
      Scenario Outline: `@rxdata.dataclass` object `evolves` pipelines on default values
      Given sample from `<source>:<dataclass>`
      Then `evolves:init:default` is satisfied with sample
      Examples: frozen and unfrozen classes decorated with `dataclass`
       | source                     | dataclass          |
       | sample/class/evolution.py | unfrozen.plain     |
       | sample/class/evolution.py | unfrozen.inherited |
       | sample/class/evolution.py | unfrozen.composed  |
       | sample/class/evolution.py | frozen.plain       |
       | sample/class/evolution.py | frozen.inherited   |
       | sample/class/evolution.py | frozen.composed    |

      @rxdataobject.evolves.init.defaults
      Scenario Outline: `@rxdata.dataclass` object evolves `rxdata.operators.typeguard` on default values with `data(evolves=rxdata.operators.typeguard(...))`
      Given sample from `<source>:<dataclass>`
      Then `typeguard:init:default` is satisfied with sample
      Examples: frozen and unfrozen classes decorated with `dataclass`
       | source                     | dataclass          |
       | sample/class/evolution.py | unfrozen.plain     |
       | sample/class/evolution.py | unfrozen.inherited |
       | sample/class/evolution.py | unfrozen.composed  |
       | sample/class/evolution.py | frozen.plain       |
       | sample/class/evolution.py | frozen.inherited   |
       | sample/class/evolution.py | frozen.composed    |


      @rxdataobject.evolves.init.kwargs
      Scenario Outline: `@rxdata.dataclass` object `evolves` on init args
      Given sample from `<source>:<dataclass>`
      Then `evolves:init:kwargs` is satisfied with sample
      Examples: frozen and unfrozen classes decorated with `dataclass`
       | source                     | dataclass          |
       | sample/class/evolution.py | unfrozen.plain     |
       | sample/class/evolution.py | unfrozen.inherited |
       | sample/class/evolution.py | unfrozen.composed  |
       | sample/class/evolution.py | frozen.plain       |
       | sample/class/evolution.py | frozen.inherited   |
       | sample/class/evolution.py | frozen.composed    |

      @rxdataobject.evolves.init.kwargs
      Scenario Outline: `@rxdata.dataclass` object evolves `rxdata.operators.typeguard` on init args with `data(evolves=rxdata.operators.typeguard(...))`
      Given sample from `<source>:<dataclass>`
      Then `typeguard:init:kwargs` is satisfied with sample
      Examples: frozen and unfrozen classes decorated with `dataclass`
       | source                     | dataclass          |
       | sample/class/evolution.py | unfrozen.plain     |
       | sample/class/evolution.py | unfrozen.inherited |
       | sample/class/evolution.py | unfrozen.composed  |
       | sample/class/evolution.py | frozen.plain       |
       | sample/class/evolution.py | frozen.inherited   |
       | sample/class/evolution.py | frozen.composed    |


      @rxdataobject.evolves.setattr
      Scenario Outline: `@rxdata.dataclass` object `evolves` pipelines on setattr
      Given sample from `<source>:<dataclass>`
      Then `evolves:setattr` is satisfied with sample
      Examples: frozen and unfrozen classes decorated with `dataclass`
       | source                     | dataclass          |
       | sample/class/evolution.py | unfrozen.plain     |
       | sample/class/evolution.py | unfrozen.inherited |
       | sample/class/evolution.py | unfrozen.composed  |
       | sample/class/evolution.py | frozen.plain       |
       | sample/class/evolution.py | frozen.inherited   |
       | sample/class/evolution.py | frozen.composed    |


      @rxdataobject.evolves.setattr
      Scenario Outline: `@rxdata.dataclass` object evolves `rxdata.operators.typeguard` on setattr with `data(evolves=rxdata.operators.typeguard(...))`
      Given sample from `<source>:<dataclass>`
      Then `typeguard:setattr` is satisfied with sample
      Examples: frozen and unfrozen classes decorated with `dataclass`
       | source                     | dataclass          |
       | sample/class/evolution.py | unfrozen.plain     |
       | sample/class/evolution.py | unfrozen.inherited |
       | sample/class/evolution.py | unfrozen.composed  |
       | sample/class/evolution.py | frozen.plain       |
       | sample/class/evolution.py | frozen.inherited   |
       | sample/class/evolution.py | frozen.composed    |
