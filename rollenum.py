from enum import Enum

Ops = Enum('add','sub','mul','div')
Fn = Enum('constant','dice','xdice','op','var_grouping','const_grouping')

StrFn = lambda x: eval('Fn.{0}'.format(x))
StrOps = lambda x: eval('Ops.{0}'.format(x))

OpsRepr = { Ops.add:'+', Ops.sub:'-', Ops.mul:'*', Ops.div:'/' }
