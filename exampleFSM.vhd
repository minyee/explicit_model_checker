--Author: Erik Anderson
--Date: 11/9/2017
--Description: Simple Moore FSM for ES Model Checker

library ieee;
use ieee.Std_Logic_1164.all;


--Entity declaration
entity exampleFSM is
  port (
    Clk 					: in Std_Logic;
    Rst 					: in Std_Logic;
	 rand_condition1	: in std_Logic;
	 rand_condition2	: in std_Logic;
	 p						: out std_Logic;
	 q						: out std_Logic
  );
end entity exampleFSM;

--Architecture declaration
architecture arc of exampleFSM is

--State enumeration
type T_States is (S0, S1, S2, S3);--last state is for testing
--Signal declarations
signal state : T_States;

begin

--Transition process statement
process(CLK)--comment
begin

if rising_edge(Clk) then
	if Rst = '1'  then
		state <= S0;
	else
		case(state) is
			when S0 =>
				if rand_condition1 = '1' then
					state <= S1;
				else
					state <= S0;
				end if;
			when S1 =>
					state <= S2;
			when S2 =>
				if rand_condition2 = '1' then
					state <= S2;
				else
					state <= S1;
				end if;
			when S3 =>
				state <= S2;
		end case;
	end if;
end if;

end process;

--Output process statement
ProceSs(state)
begin

case(state) is
	when S0 =>
		p <= '1';
		q <= '0';
	when S1 =>
		p <= '0';
		q <= '1';
	when S2 =>
		p <= '1';
		q <= '1';
	when S3 =>
		p <= '0';
		q <= '0';
end case;

end process;


end arc;
