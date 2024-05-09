
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'programBRACKETDER BRACKETIZQ COMA COMILLAS CORCHETEDER CORCHETEIZQ CTE_FLOAT CTE_INT CTE_STRING DIV DO DOSPUNTOS ELSE END EXCLAMACION FLOAT ID IF IGUAL INT MAIN MAYORQUE MENORQUE MINUS MULT PARENDER PARENIZQ PLUS PRINT PROGRAM PUNTO PUNTOCOMA VAR VOID WHILEprogram : PROGRAM ID PUNTOCOMA vars_opt funcs_opt MAIN ENDvars_opt : vars \n    | emptyvars : VAR vars_1vars_1 : id DOSPUNTOS type PUNTOCOMA \n    | emptyid : ID id_1id_1 : COMA id\n    | emptytype : INT\n    | FLOATfuncs_opt : funcs funcs_opt\n    | emptyfuncs : VOID ID PARENIZQ params PARENDER PUNTOCOMAparams : params_1\n    | emptyparams_1 : ID DOSPUNTOS type params_cycleparams_cycle : COMA params_1\n    | emptyempty :'
    
_lr_action_items = {'PROGRAM':([0,],[2,]),'$end':([1,24,],[0,-1,]),'ID':([2,8,12,22,25,40,],[3,16,19,16,30,30,]),'PUNTOCOMA':([3,26,27,28,36,],[4,34,-10,-11,38,]),'VAR':([4,],[8,]),'VOID':([4,5,6,7,8,10,13,15,34,38,],[-20,12,-2,-3,-20,12,-4,-6,-5,-14,]),'MAIN':([4,5,6,7,8,9,10,11,13,15,18,34,38,],[-20,-20,-2,-3,-20,17,-20,-13,-4,-6,-12,-5,-14,]),'DOSPUNTOS':([14,16,21,23,29,30,],[20,-20,-7,-9,-8,35,]),'COMA':([16,27,28,37,],[22,-10,-11,40,]),'END':([17,],[24,]),'PARENIZQ':([19,],[25,]),'INT':([20,35,],[27,27,]),'FLOAT':([20,35,],[28,28,]),'PARENDER':([25,27,28,31,32,33,37,39,41,42,],[-20,-10,-11,36,-15,-16,-20,-17,-19,-18,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'vars_opt':([4,],[5,]),'vars':([4,],[6,]),'empty':([4,5,8,10,16,25,37,],[7,11,15,11,23,33,41,]),'funcs_opt':([5,10,],[9,18,]),'funcs':([5,10,],[10,10,]),'vars_1':([8,],[13,]),'id':([8,22,],[14,29,]),'id_1':([16,],[21,]),'type':([20,35,],[26,37,]),'params':([25,],[31,]),'params_1':([25,40,],[32,42,]),'params_cycle':([37,],[39,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> PROGRAM ID PUNTOCOMA vars_opt funcs_opt MAIN END','program',7,'p_program','parser_.py',6),
  ('vars_opt -> vars','vars_opt',1,'p_vars_opt','parser_.py',10),
  ('vars_opt -> empty','vars_opt',1,'p_vars_opt','parser_.py',11),
  ('vars -> VAR vars_1','vars',2,'p_vars','parser_.py',18),
  ('vars_1 -> id DOSPUNTOS type PUNTOCOMA','vars_1',4,'p_vars_1','parser_.py',22),
  ('vars_1 -> empty','vars_1',1,'p_vars_1','parser_.py',23),
  ('id -> ID id_1','id',2,'p_id','parser_.py',30),
  ('id_1 -> COMA id','id_1',2,'p_id_1','parser_.py',34),
  ('id_1 -> empty','id_1',1,'p_id_1','parser_.py',35),
  ('type -> INT','type',1,'p_type','parser_.py',42),
  ('type -> FLOAT','type',1,'p_type','parser_.py',43),
  ('funcs_opt -> funcs funcs_opt','funcs_opt',2,'p_funcs_opt','parser_.py',47),
  ('funcs_opt -> empty','funcs_opt',1,'p_funcs_opt','parser_.py',48),
  ('funcs -> VOID ID PARENIZQ params PARENDER PUNTOCOMA','funcs',6,'p_funcs','parser_.py',55),
  ('params -> params_1','params',1,'p_params','parser_.py',59),
  ('params -> empty','params',1,'p_params','parser_.py',60),
  ('params_1 -> ID DOSPUNTOS type params_cycle','params_1',4,'p_params_1','parser_.py',67),
  ('params_cycle -> COMA params_1','params_cycle',2,'p_params_cycle','parser_.py',71),
  ('params_cycle -> empty','params_cycle',1,'p_params_cycle','parser_.py',72),
  ('empty -> <empty>','empty',0,'p_empty','parser_.py',79),
]
