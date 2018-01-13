	CREATE OR REPLACE FUNCTION state_group_and_count( state map<text, int>, type text ) CALLED ON NULL INPUT RETURNS map<text, int>
	LANGUAGE java AS 'Integer count = (Integer) state.get(type);  if (count == null) count = 1; else count++; state.put(type, count); return state; ';
	
	CREATE OR REPLACE FUNCTION final_group_and_count( state map<text, int> ) CALLED ON NULL INPUT RETURNS map<text, int>
	LANGUAGE java AS 'return state; ';
	
	CREATE OR REPLACE AGGREGATE group_and_count(text) 
	SFUNC state_group_and_count 
	STYPE map<text, int> 
	FINALFUNC final_group_and_count 
	INITCOND {};
	
Equivalent à, la fonction de reduce pourrait servir à trouver le plus représenté des éléments.
	
	CREATE OR REPLACE FUNCTION state_group_and_count( state map<text, int>, type text ) CALLED ON NULL INPUT RETURNS map<text, int>
	LANGUAGE java AS 'Integer count = (Integer) state.get(type);  if (count == null) count = 1; else count++; state.put(type, count); return state; ';
	
	CREATE OR REPLACE AGGREGATE group_and_count(text) 
	SFUNC state_group_and_count 
	STYPE map<text, int> 
	INITCOND {};

Autre exemple :

	CREATE OR REPLACE FUNCTION state_group_and_max(state map<text, int>, type text, amount int)
	  CALLED ON NULL INPUT
	  RETURNS map<text, int>
	  LANGUAGE java AS '
	    Integer val = (Integer) state.get(type);
	    if (val == null) val = amount; else val = Math.max(val, amount);
	    state.put(type, val);
	    return state;
	  ' ;
	
	CREATE OR REPLACE AGGREGATE state_group_and_max(text, int) 
	  SFUNC state_group_and_max
	  STYPE map<text, int> 
	  INITCOND {};