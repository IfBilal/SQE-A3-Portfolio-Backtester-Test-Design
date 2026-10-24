RUN_OK = 'Accepted; calculation completes'
REJ = 'Rejected with a validation message; no calculation is run'
BC = []
def B(form, field, ecref, desc, bval, cases):
    BC.append((form, field, ecref, desc, bval, cases))
B('BT','Starting Value','Zero/fractional starting value (IEC) vs valid starting value (VEC)','Minimum starting value','1',
  [('0.99','Below',[['#4','0.99']],REJ,'native'),('1','At',[['#4','1']],RUN_OK,'run'),('2','Above',[['#4','2']],RUN_OK,'run')])
B('BT','Starting Value','Starting value above the upper limit (IEC) vs valid (VEC)','Maximum starting value (largest accepted)','999,999,999,999',
  [('999,999,999,998','Below',[['#4','999999999998']],RUN_OK,'run'),('999,999,999,999','At',[['#4','999999999999']],RUN_OK,'run'),('1,000,000,000,000','Above',[['#4','1000000000000']],REJ,'toast')])
B('BT','Rolling Window','Zero rolling window (IEC) vs valid (VEC)','Minimum rolling window (months)','1',
  [('0','Below',[['#6','0']],REJ,'native'),('1','At',[['#6','1']],RUN_OK,'run'),('2','Above',[['#6','2']],RUN_OK,'run')])
B('BT','Rolling Window','Rolling window above the upper limit (IEC) vs valid (VEC)','Maximum rolling window (largest accepted)','11999',
  [('11998','Below',[['#6','11998']],RUN_OK,'run'),('11999','At',[['#6','11999']],RUN_OK,'run'),('12000','Above',[['#6','12000']],REJ,'toast')])
B('BT','Annual cashflow growth','Growth below minimum (IEC) vs valid (VEC)','Minimum annual cashflow growth (%)','-99.99',
  [('-100','Below',[['#10','-100']],REJ,'native'),('-99.99','At',[['#10','-99.99']],RUN_OK,'run'),('-99.98','Above',[['#10','-99.98']],RUN_OK,'run')])
B('BT','Annual cashflow growth','Growth above maximum (IEC) vs valid (VEC)','Maximum annual cashflow growth (%)','100',
  [('99.99','Below',[['#10','99.99']],RUN_OK,'run'),('100','At',[['#10','100']],RUN_OK,'run'),('100.01','Above',[['#10','100.01']],REJ,'native')])
B('BT','Allocation % (portfolio total)','Allocations sum below/above 100 (IEC) vs sum = 100 (VEC)','Required allocation total (%)','100',
  [('99.99 (60/39.99)','Below',[['#25','39.99']],REJ,'toast'),('100 (60/40)','At',[],RUN_OK,'run'),('100.01 (60/40.01)','Above',[['#25','40.01']],REJ,'toast')])
B('BT','Start Date / End Date','Start after end date (IEC) / start equal end (IEC) vs start before end (VEC)','Start date must be strictly before end date (end relative to start 2020-01-01)','end = start + 1 day',
  [('end 2019-12-31','Below',[['#2','2020-01-01'],['#3','2019-12-31']],REJ,'toast'),('end 2020-01-01','At',[['#2','2020-01-01'],['#3','2020-01-01']],REJ,'toast'),('end 2020-01-02','Above',[['#2','2020-01-01'],['#3','2020-01-02']],RUN_OK,'run')])
B('BT','Drag (annual fee %)','Negative drag (IEC) vs valid drag (VEC)','Lower limit of drag (expected 0%)','0',
  [('-1','Below',[['#19','-1']],REJ,'run_bad'),('0','At',[['#19','0']],RUN_OK,'run'),('1','Above',[['#19','1']],RUN_OK,'run')])
B('BT','Drag (annual fee %)','Drag above 100% (IEC) vs valid drag (VEC)','Upper limit of drag (expected 100%)','100',
  [('99','Below',[['#19','99']],RUN_OK,'run'),('100','At',[['#19','100']],RUN_OK,'run'),('101','Above',[['#19','101']],REJ,'run_bad')])
B('MC','Number of years','Horizon below minimum (IEC) vs valid (VEC)','Minimum horizon (years)','1',
  [('0','Below',[['Number of years','0']],REJ,'native'),('1','At',[['Number of years','1']],RUN_OK,'run')])
B('MC','Number of years','Horizon above free-plan limit (IEC) vs valid (VEC)','Free-plan maximum horizon (years)','15',
  [('15','At',[['Number of years','15']],RUN_OK,'run'),('16','Above',[['Number of years','16']],'Rejected or plan-limit message','gate')])
B('MC','Number of years','Horizon above absolute maximum (IEC)','Absolute maximum horizon (years)','100',
  [('100','At',[['Number of years','100']],'Accepted (paid plan) or plan-limit message on Free','gate'),('101','Above',[['Number of years','101']],REJ,'native')])
B('MC','Starting Value','Zero starting value (IEC) vs valid (VEC)','Minimum starting value','1',
  [('0','Below',[['Starting Value','0']],REJ,'native'),('1','At',[['Starting Value','1']],RUN_OK,'run')])
B('MC','Min block (years)','Minimum block below minimum (IEC) vs valid (VEC)','Minimum value of Min block (years)','0.05',
  [('0.04','Below',[['Min block','0.04']],REJ,'native'),('0.05','At',[['Min block','0.05']],RUN_OK,'run')])
B('MC','Max block (years)','Maximum block above maximum (IEC) vs valid (VEC)','Maximum value of Max block (years)','20',
  [('20','At',[['Max block','20']],RUN_OK,'run'),('21','Above',[['Max block','21']],REJ,'native')])
B('MC','Random seed','Negative seed (IEC) vs valid (VEC)','Minimum random seed','0',
  [('-1','Below',[['Random seed','-1']],REJ,'native'),('0','At',[['Random seed','0']],RUN_OK,'run')])
B('SW','Retirement horizon (years)','Zero horizon (IEC) vs valid (VEC)','Minimum retirement horizon (years)','1',
  [('0','Below',[['#6','0']],REJ,'toast'),('2 (Phase 1 end 1)','At',[['#6','2'],['#7','1']],RUN_OK,'run')])
B('SW','Retirement horizon (years)','Horizon above maximum (IEC) vs valid (VEC)','Maximum retirement horizon (years)','50',
  [('50','At',[['#6','50']],RUN_OK,'run'),('51','Above',[['#6','51']],REJ,'native')])
B('SW','Phase 1 end year','End year zero (IEC) vs valid (VEC)','Minimum Phase 1 end year','1',
  [('0','Below',[['#7','0']],REJ,'toast'),('1','At',[['#7','1']],RUN_OK,'run')])
B('SW','Phase 1 end year','End year not before horizon (IEC) vs valid (VEC)','Phase 1 end year must be below the horizon (horizon 30)','29',
  [('29','At',[['#7','29']],RUN_OK,'run'),('30','Above',[['#7','30']],REJ,'toast')])
B('SW','Phase 1 annual withdrawal %','Negative rate (IEC) vs valid (VEC)','Minimum Phase 1 withdrawal rate (%)','0',
  [('-1','Below',[['#8','-1']],REJ,'native'),('0','At',[['#8','0']],RUN_OK,'run')])
B('SW','Phase 1 annual withdrawal %','Rate above 100 (IEC) vs valid (VEC)','Maximum Phase 1 withdrawal rate (%)','100',
  [('100','At',[['#8','100']],RUN_OK,'run'),('101','Above',[['#8','101']],REJ,'native')])
B('SW','Phase 2 annual withdrawal %','Negative rate (IEC) vs valid (VEC)','Minimum Phase 2 withdrawal rate (%)','0',
  [('-1','Below',[['#10','-1']],REJ,'native'),('0','At',[['#10','0']],RUN_OK,'run')])
B('SW','Phase 2 annual withdrawal %','Rate above 100 (IEC) vs valid (VEC)','Maximum Phase 2 withdrawal rate (%)','100',
  [('100','At',[['#10','100']],RUN_OK,'run'),('101','Above',[['#10','101']],REJ,'native')])
T=['Tickers','SPY AGG GLD']
B('OP','Starting Value','Zero starting value (IEC) vs valid (VEC)','Minimum starting value','1',
  [('0','Below',[T,['Starting Value','0']],REJ,'native'),('1','At',[T,['Starting Value','1']],RUN_OK,'run')])
B('OP','Rolling Window','Zero rolling window (IEC) vs valid (VEC)','Minimum rolling window (months)','1',
  [('0','Below',[T,['Rolling Window','0']],REJ,'native'),('1','At',[T,['Rolling Window','1']],RUN_OK,'run')])
B('OP','Max holdings','Zero max holdings (IEC) vs valid (VEC)','Minimum max holdings','1',
  [('0','Below',[T,['Max holdings','0']],REJ,'native'),('1','At',[T,['Max holdings','1']],RUN_OK,'run')])
B('OP','Min weight to include (%)','Negative minimum weight (IEC) vs valid (VEC)','Minimum value of min weight (%)','0',
  [('-1','Below',[T,['Min weight to include','-1']],REJ,'native'),('0','At',[T,['Min weight to include','0']],RUN_OK,'run')])
B('OP','Min weight to include (%)','Minimum weight above 100 (IEC) vs valid (VEC)','Maximum value of min weight (%)','100',
  [('100','At',[T,['Min weight to include','100']],RUN_OK,'run'),('101','Above',[T,['Min weight to include','101']],REJ,'native')])
B('OP','Max vol (%)','Negative max vol (IEC) vs valid (VEC)','Minimum value of max vol (%)','0',
  [('-1','Below',[T,['Max vol','-1']],REJ,'native'),('0','At',[T,['Max vol','0']],'Accepted (may report no feasible solution)','run_any')])
B('OP','Tickers','One ticker (IEC) vs two tickers (VEC)','Minimum number of tickers','2',
  [('1 ticker (SPY)','Below',[['Tickers','SPY']],REJ,'toast'),('2 tickers (SPY AGG)','At',[['Tickers','SPY AGG']],RUN_OK,'run')])
B('EF','Tickers','One ticker (IEC) vs two tickers (VEC)','Minimum number of tickers','2',
  [('1 ticker (SPY)','Below',[['Tickers','SPY']],REJ,'toast'),('2 tickers (SPY AGG)','At',[['Tickers','SPY AGG']],RUN_OK,'run')])
B('EF','Tickers','Three tickers on Free plan (IEC) vs two (VEC)','Free-plan maximum number of tickers','2',
  [('2 tickers (SPY AGG)','At',[['Tickers','SPY AGG']],RUN_OK,'run'),('3 tickers (SPY AGG GLD)','Above',[['Tickers','SPY AGG GLD']],'Rejected or plan-limit message','gate')])
B('EF','Max holdings','Zero max holdings (IEC) vs valid (VEC)','Minimum max holdings','1',
  [('0','Below',[['Tickers','SPY AGG'],['Max holdings','0']],REJ,'native'),('1','At',[['Tickers','SPY AGG'],['Max holdings','1']],RUN_OK,'run')])
B('EF','Min weight to include (%)','Negative minimum weight (IEC) vs valid (VEC)','Minimum value of min weight (%)','0',
  [('-1','Below',[['Tickers','SPY AGG'],['Min weight to include','-1']],REJ,'native'),('0','At',[['Tickers','SPY AGG'],['Min weight to include','0']],RUN_OK,'run')])
B('EF','Min weight to include (%)','Minimum weight above 100 (IEC) vs valid (VEC)','Maximum value of min weight (%)','100',
  [('100','At',[['Tickers','SPY AGG'],['Min weight to include','100']],RUN_OK,'run'),('101','Above',[['Tickers','SPY AGG'],['Min weight to include','101']],REJ,'native')])
LDB=[['#15','SPY'],['#16','60'],['#17','AGG'],['#18','40']]
B('LD','Starting Value','Starting value below minimum (IEC) vs valid (VEC)','Minimum starting value','100',
  [('99','Below',LDB+[['Starting Value','99']],REJ,'native'),('100','At',LDB+[['Starting Value','100']],'Input accepted by validation','gate')])
B('LD','DCA horizon (months)','Horizon below minimum (IEC) vs valid (VEC)','Minimum DCA horizon (months)','1',
  [('0','Below',LDB+[['DCA horizon','0']],REJ,'native'),('1','At',LDB+[['DCA horizon','1']],'Input accepted by validation','gate')])
B('LD','DCA horizon (months)','Horizon above maximum (IEC) vs valid (VEC)','Maximum DCA horizon (months)','120',
  [('120','At',LDB+[['DCA horizon','120']],'Input accepted by validation','gate'),('121','Above',LDB+[['DCA horizon','121']],REJ,'native')])
B('TV','Starting Value','Negative starting value (IEC) vs valid (VEC)','Minimum starting value','0',
  [('-1','Below',[['Starting Value','-1']],REJ,'toast'),('0','At',[['Starting Value','0']],RUN_OK,'run')])
B('TV','Starting Value','Starting value above maximum (IEC) vs valid (VEC)','Maximum starting value','5,000,000',
  [('5,000,000','At',[['Starting Value','5000000']],RUN_OK,'run'),('5,000,001','Above',[['Starting Value','5000001']],REJ,'toast')])
B('TV','Monthly contribution','Negative contribution (IEC) vs valid (VEC)','Minimum monthly contribution','0',
  [('-1','Below',[['Monthly contribution','-1']],REJ,'toast'),('0','At',[['Monthly contribution','0']],RUN_OK,'run')])
B('TV','Monthly contribution','Contribution above maximum (IEC) vs valid (VEC)','Maximum monthly contribution','100,000',
  [('100,000','At',[['Monthly contribution','100000']],RUN_OK,'run'),('100,001','Above',[['Monthly contribution','100001']],REJ,'toast')])
B('CT','Name','Name longer than 120 characters (IEC) vs valid (VEC)','Maximum name length','120',
  [('120 chars','At',[],'Accepted','pending'),('121 chars','Above',[],'Rejected or truncated at 120','pending')])
B('CT','Subject','Subject longer than 120 characters (IEC) vs valid (VEC)','Maximum subject length','120',
  [('120 chars','At',[],'Accepted','pending'),('121 chars','Above',[],'Rejected or truncated at 120','pending')])
B('CT','Message','Message longer than 5000 characters (IEC) vs valid (VEC)','Maximum message length','5000',
  [('5000 chars','At',[],'Accepted','pending'),('5001 chars','Above',[],'Rejected or truncated at 5000','pending')])
B('SU','Password','Password shorter than minimum (IEC) vs valid (VEC)','Minimum password length','8 characters',
  [('7 chars','Below',[],'Rejected; too short','pending'),('8 chars','At',[],'Accepted','pending')])
