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
type T_States is (S0, S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13);
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
				state <= S1;
			when S1 =>
        if rand_condition2 = '1' then
          state <= S2;
        elsif rand_condition1 = '1' then
          state <= S4;
        else
          state <= S5;
        end if;
			when S2 =>
        if rand_condition2 = '1' then
          state <= S3;
        else
          state <= S6;
        end if;
			when S3 =>
        if rand_condition2 = '1' then
          state <= S2;
        else
          state <= S7;
        end if;
      when S4 =>
        if rand_condition2 = '1' then
          state <= S0;
        else
          state <= S5;
        end if;
  		when S5 =>
  		  state <= S6;
  		when S6 =>
        state <= S5;
  		when S7 =>
        if rand_condition2 = '1' then
          state <= S3;
        elsif rand_condition1 = '1' then
          state <= S6;
        else
          state <= S11;
        end if;
      when S8 =>
    	 state <= S3;
    	when S9 =>
        if rand_condition2 = '1' then
          state <= S8;
        else
          state <= S10;
        end if;
    	when S10 =>
        if rand_condition2 = '1' then
          state <= S8;
        elsif rand_condition1 = '1' then
          state <= S12;
        else
          state <= S13;
        end if;
    	when S11 =>
        if rand_condition2 = '1' then
          state <= S7;
        elsif rand_condition1 = '1' then
          state <= S8;
        else
          state <= S12;
        end if;
      when S12 =>
      	if rand_condition2 = '1' then
      		state <= S9;
      	else
      		state <= S13;
      	end if;
      when S13 =>
      	state <= S13;
		end case;
	end if;
end if;

end process;

--Output process statement
Process(state)
begin

case(state) is
  when S0 =>
      p <= '1';
      q <= '0';
  when S1 =>
      p <= '1';
      q <= '0';
  when S2 =>
      p <= '1';
      q <= '0';
  when S3 =>
      p <= '1';
      q <= '0';
  when S4 =>
      p <= '1';
      q <= '0';
  when S5 =>
      p <= '1';
      q <= '0';
  when S6 =>
      p <= '1';
      q <= '0';
  when S7 =>
      p <= '1';
      q <= '0';
  when S8 =>
      p <= '1';
      q <= '0';
  when S9 =>
      p <= '0';
      q <= '0';
  when S10 =>
      p <= '1';
      q <= '0';
  when S11 =>
      p <= '0';
      q <= '0';
  when S12 =>
      p <= '1';
      q <= '0';
  when S13 =>
      p <= '0';
      q <= '0';
end case;

end process;


end arc;
