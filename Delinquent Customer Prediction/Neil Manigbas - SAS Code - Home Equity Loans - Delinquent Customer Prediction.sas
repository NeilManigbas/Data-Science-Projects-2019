libname tt "/home/u38421560/TT";

data tt.hmeq;
   set sampsio.hmeq;
run;

/* Understand your data */
proc contents data=tt.Hmeq;
run;

/*
	 #    Variable    Type    Len    Label

	 1    bad         Num       8    Default or seriously delinquent
	10    clage       Num       8    Age of oldest trade line in months
	12    clno        Num       8    Number of trade (credit) lines
	13    debtinc     Num       8    Debt to income ratio
	 9    delinq      Num       8    Number of delinquent trade lines
	 8    derog       Num       8    Number of major derogatory reports
	 6    job         Char      6    Prof/exec sales mngr office self other
	 2    loan        Num       8    Amount of current loan request
	 3    mortdue     Num       8    Amount due on existing mortgage
	11    ninq        Num       8    Number of recent credit inquiries
	 5    reason      Char      7    Home improvement or debt consolidation
	 4    value       Num       8    Value of current property
	 7    yoj         Num       8    Years on current job

*/

proc print data=tt.Hmeq (obs=15);
run;

/* Focus on the Char variables */
proc freq data=tt.hmeq;
   tables reason job;
run;

/* Convert Char var to NUM var on the data of Dev*/
/* Creating dummy variable for Char variables */
data tt.Hmeq(drop=job reason);
  set tt.Hmeq;
  JOB_Mgr=(JOB='Mgr');
  JOB_Office=(JOB='Office');
  JOB_Other=(JOB='Other');
  JOB_ProfExe=(JOB='ProfExe');
  JOB_Sales=(JOB='Sales');
  JOB_Self=(JOB='Self');
  JOB_miss=(JOB=' ');
  REASON_DebtCon=(REASON='DebtCon');
  REASON_HomeImp=(REASON='HomeImp');
  REASON_Miss=(REASON=' ');

run;

proc contents data=tt.Hmeq;
run;

/* Data preperation */
%let inter_var=
clage
clno
debtinc
delinq
derog
loan
mortdue
ninq
value
yoj
;

%let DSN=tt.Hmeq;
%let RESP=BAD;
%let GROUPS=20;
run;

/* Creating Macro Function to plot response versus variables,
	determine values to impute to missing items and
		add a new column with LOG values */
%MACRO LOGTCONT;
      OPTIONS CENTER PAGENO=1 DATE;
	  data test;
	    set &DSN;
	  run;
	  %do i=1 %to 10;
	  %LET VBLE=%scan(&inter_var, &i);  
       PROC RANK DATA =TEST (KEEP=&RESP &VBLE)
               GROUPS = &GROUPS
                  OUT = JUNK1;
            RANKS NEWVBLE;
            VAR &VBLE;
       RUN;

       PROC SUMMARY DATA = JUNK1 NWAY;
            CLASS NEWVBLE;
            VAR &RESP &VBLE;
            OUTPUT OUT = JUNK2
                  MEAN =
                  MIN(&VBLE)=MIN
                  MAX(&VBLE)=MAX
                     N = NOBS;
       RUN;

       DATA JUNK2;
            SET JUNK2;
            IF &RESP NE 0 THEN
               LOGIT = LOG (&RESP / (1- &RESP));
            ELSE IF &RESP = 0 THEN LOGIT = .;
       RUN;

       PROC SQL NOPRINT;
        CREATE TABLE JUNK3 AS
        SELECT 99 AS NEWVBLE, COUNT(*) AS NOBS, MEAN(&RESP) AS &RESP
        FROM test
        WHERE &VBLE=.;

       DATA JUNK3;
        SET JUNK3;
        LOGIT=LOG(&RESP/(1-&RESP));
       RUN;

       DATA JUNK4;
        SET JUNK2 JUNK3;
       RUN;

       PROC PLOT DATA = JUNK4;
            TITLE1 "Plot of Logit(Response) by &&VBLE";
            PLOT  LOGIT* &VBLE;
       RUN;

       PROC PLOT DATA=JUNK4;
       PLOT &RESP*&VBLE;
       PLOT _FREQ_*&VBLE;
       TITLE2 "PLOT OF RESPONSE BY &&VBLE";
       RUN;

       PROC PRINT DATA = JUNK4 LABEL SPLIT = '*' NOOBS;
            TITLE3 "Table of Response by Grouped &&VBLE";
            VAR NEWVBLE NOBS &VBLE MIN MAX &RESP;
            LABEL NEWVBLE = "&&VBLE Grouping"
                     NOBS = '# of*Records'
                     LOGIT = "Logit of Response"
                     MIN   ='MIN'
                     MAX   ='MAX';
       RUN;

	   %end;


%MEND LOGTCONT;
%LOGTCONT;

/* Do data transformation on the data set */
/* Fill the missing values for numerical values */
data tt.Hmeq;
  set tt.Hmeq;
  if CLAGE=. then CLAGE=100.561;
  if CLAGE>321 then CLAGE=321;
  *if CLNO<10 then CLNO=0;
  if CLNO=. then CLNO= 47.6;
  *if CLNO<15 then CLNO= 15;
     DEBTINC_MISS=(DEBTINC=.);
  if DELINQ=. then DELINQ=0;
  if DEROG=. then DEROG=0;
  if LOAN>40000 then LOAN=40000;
  if MORTDUE=. then MORTDUE= 67469.76;
  if NINQ=. then NINQ=0;
     VALUE_MISS=(VALUE=.);
  if YOJ=. then YOJ=0;
run;

PROC CONTENTS DATA=tt.Hmeq;
RUN;

/* Split data into two parts (Dev and Val) */
data MODEL_DEV MODEL_VAL;
  set tt.Hmeq;
  if ranuni(1234567)<=0.6 THEN OUTPUT MODEL_DEV;
  ELSE                         OUTPUT MODEL_VAL;
run;

proc sql;
select count(*) as MODEL_DEV from MODEL_DEV;
select count(*) as MODEL_VAL from MODEL_VAL;
select count(*) as HMEQ_Dataset from tt.Hmeq;
run;

/* Finalize the variables which are included in the final model using Stepwise selection procedure */
%LET INPUT=
JOB_Mgr
JOB_Office
JOB_Other
JOB_ProfExe
JOB_Sales
JOB_Self
JOB_miss
REASON_DebtCon
REASON_HomeImp
REASON_Miss
clage
clno
DEBTINC_MISS
delinq
derog
loan
mortdue
ninq
VALUE_MISS
yoj
;

proc logistic data=MODEL_DEV descending;
model bad=&input
  /selection=stepwise fast lackfit rsquare corrb stb;
run;


/* Apply model equation to the data of Val */
data val;
  set MODEL_VAL;

Logit=
-1.5316			
-0.4294		*	JOB_Office		
+0.9378		*	JOB_Sales		
-2.1034		*	JOB_miss		
-0.2633		*	REASON_DebtCon	
-0.00770	*	CLAGE			
+2.6637		*	DEBTINC_MISS	
+0.6708		*	DELINQ			
+0.5878		*	DEROG			
+0.1293		*	NINQ			
+4.2212		*	VALUE_MISS
;

prob=1/(1+exp(-logit)); 
run;

/* Create the lift chart to evaluate the performance of the model */
proc sort data=val out=val1;
   by descending prob;
run;

proc rank		data = val1
				out = val_ranked
				groups = 20
				descending;
		var		prob;
		ranks	rank;
run;

data val_ranked(drop=rank prob);
set val_ranked;
	model_rank=rank + 1;
	model_score=prob;
	
run;

ods csv body='rank2.csv';
PROC TABULATE DATA = val_ranked MISSING NOSEPS;
            CLASS model_rank        ;
            VAR   model_score     bad  ;
	TABLES model_rank=' ' ALL, model_score*MEAN*F=5.3 
           bad='BAD'*(sum='# of Bad' n='# of Acct' mean*F=5.3)/box='Rank';
RUN;
ods csv close;

/* Max-KS test for Model Validation - Graph presentation */
proc sort data=val out=val1;
   by descending prob;
run;

options mprint;
%macro charts(role=);

%let ds=val1;			/*output dataset from proc logistic*/                 
%let response=bad;		/*response variable */

proc rank data = &ds out = gar;
 where prob^=.;
 var prob;
 ranks rp;
run;


proc sql;
  select count(*) as tot_obs,
         sum(&response=1) as resp1,
         sum(&response=0) as resp0,
         mean(&response) as resprate
  into :tot_obs, :resp1, :resp0, :resprate
  from gar;
quit;


proc sort data = &ds out=preds1 (keep=prob &response);
 where prob^=.;
 by descending prob;
run;

/* Lift chart and Moving Avg(Gains Chart) */
%let ds=val1;                
%let response=bad;

data lft (keep=c_resp c_perf c_obs &response prob t_resp m_avg c_prob avg_resp);
 set preds1;

 if _n_ le &resp1 then c_perf = _n_ / &resp1;
 else                  c_perf = 1;

 if &response = 1 then 
 do;
   t_resp+1;
   c_resp = t_resp/&resp1;
 end;
 c_obs = _n_ / &tot_obs;

 c_prob + prob;
 m_avg=c_prob/_n_;

 avg_resp = &resprate;

 attrib
        c_resp label = 'Cumulative Response'
        m_avg  label = 'Predicted Prob'
        c_prob label = 'Cumulative Predicted Prob'
        c_obs  label = 'Cumulative Population';
run;

/* Lift Chart */
proc plot data = lft;
 plot (c_resp  c_obs)*c_obs='*' /overlay;
                              
 label c_obs='Cumulative Population'
       c_resp='Cumulative Response';
 
*title "Lift Chart - &role";
run;
title;

/* Moving Avg. */
proc plot data = lft;
 plot (m_avg avg_resp )*c_obs='*' / overlay ;
 format m_avg c_obs avg_resp percent6.;
 title "Gains Chart - &role";
run;
title;

proc datasets library=work;
  delete preds1 gar lft;
quit;

%mend;

%charts(role=model)

/*
label bad    ="Default or seriously delinquent"
      reason ="Home improvement or debt consolidation"
      job    ="Prof/exec sales mngr office self other"
      loan   ="Amount of current loan request"
      mortdue="Amount due on existing mortgage"
      value  ="Value of current property"
      debtinc="Debt to income ratio"
      yoj    ="Years on current job"
      derog  ="Number of major derogatory reports"
      clno   ="Number of trade (credit) lines"
      delinq ="Number of delinquent trade lines"
      clage  ="Age of oldest trade line in months"
      ninq   ="Number of recent credit inquiries"
      ;
*/

