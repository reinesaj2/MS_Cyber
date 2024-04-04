---------------------- MODULE HourClock ----------------------
EXTENDS Naturals
(* Abraham J. Reines, 03/31/2024 *)
VARIABLE hr
HCini  ==  hr \in (1 .. 12)
HCnxt  ==  hr' = IF hr # 12 THEN hr + 1 ELSE 1
HC  ==  HCini /\ [][HCnxt]_hr
--------------------------------------------------------------
THEOREM  HC => []HCini
==============================================================