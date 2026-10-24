FORMS = [
 ('SU', 'Sign Up', 'testfol.io/start'),
 ('SI', 'Sign In', 'testfol.io/login'),
 ('BT', 'Portfolio Backtester', 'testfol.io/'),
 ('MC', 'Monte Carlo Simulator', 'testfol.io/monte-carlo'),
 ('SW', 'Safe Withdrawal Rate Calculator', 'testfol.io/safe-withdrawal-rate-calculator'),
 ('OP', 'Backtest Optimizer', 'testfol.io/backtest-optimizer'),
 ('EF', 'Efficient Frontier', 'testfol.io/efficient-frontier'),
 ('CT', 'Contact Form', 'testfol.io/contact'),
 ('LD', 'Lump Sum vs DCA', 'testfol.io/lumpsum-vs-dca'),
 ('TV', 'Time Value of Money Calculator', 'testfol.io/time-value-of-money'),
 ('RB', 'Rebalancing Sensitivity', 'testfol.io/rebalancing-sensitivity'),
]
RUN_OK = 'Accepted; calculation/analysis completes and results are shown'
REJ = 'Rejected with a validation message; no calculation is run'
GATE_OK = 'Input accepted by validation (no validation error); analysis would run'
FIELDS = []
def F(form, field, rows):
    FIELDS.append((form, field, rows))

F('SU','Email',[
 ('Valid, unregistered email address format','newuser@example.com','VEC','Account created / verification step shown',[],'pending'),
 ('Empty email','(empty)','IEC','Rejected; email required',[],'pending'),
 ('Email without @ symbol','notanemail','IEC','Rejected; invalid email format',[],'pending'),
 ('Email without domain suffix','a@b','IEC','Rejected; invalid email format',[],'pending'),
 ('Email already registered','(your registered email)','IEC','Rejected; account exists',[],'pending')])
F('SU','Password',[
 ('Password of valid length','Test@1234','VEC','Accepted',[],'pending'),
 ('Empty password','(empty)','IEC','Rejected; password required',[],'pending'),
 ('Password shorter than minimum length','abcde','IEC','Rejected; too short',[],'pending'),
 ('Password longer than maximum length','73 x a','IEC','Rejected or truncated; too long',[],'pending')])
F('SI','Email',[
 ('Registered email','(your registered email)','VEC','Accepted',[],'pending'),
 ('Empty email','(empty)','IEC','Rejected; email required',[],'pending'),
 ('Malformed email','notanemail','IEC','Rejected; invalid email format',[],'pending'),
 ('Unregistered email','nobody@x.com','IEC','Rejected; invalid credentials',[],'pending')])
F('SI','Password',[
 ('Correct password for the account','(correct password)','VEC','Signed in',[],'pending'),
 ('Empty password','(empty)','IEC','Rejected; password required',[],'pending'),
 ('Wrong password','wrongpass1234','IEC','Rejected; invalid credentials',[],'pending')])
F('CT','Name',[
 ('Valid name (1-120 chars)','Muhammad Bilal Tahir','VEC','Accepted',[],'pending'),
 ('Empty name','(empty)','IEC','Rejected; name required',[],'pending'),
 ('Name longer than 120 characters','121 x a','IEC','Input limited/rejected at 120',[],'pending')])
F('CT','Email',[
 ('Valid email format','student@example.com','VEC','Accepted',[],'pending'),
 ('Empty email','(empty)','IEC','Rejected; email required',[],'pending'),
 ('Malformed email','notanemail','IEC','Rejected; invalid format',[],'pending')])
F('CT','Subject',[
 ('Valid subject (1-120 chars)','Question about backtests','VEC','Accepted',[],'pending'),
 ('Empty subject','(empty)','IEC','Rejected; subject required',[],'pending'),
 ('Subject longer than 120 characters','121 x a','IEC','Input limited/rejected at 120',[],'pending')])
F('CT','Message',[
 ('Valid message (1-5000 chars)','Hello, test message','VEC','Accepted',[],'pending'),
 ('Empty message','(empty)','IEC','Rejected; message required',[],'pending'),
 ('Message longer than 5000 characters','5001 x a','IEC','Input limited/rejected at 5000',[],'pending')])

BT='BT'
F(BT,'Start Date',[
 ('Valid start date inside data range, before end date','2020-01-01 (end 2021-01-01)','VEC','Backtest runs for the entered period',[['#2','2020-01-01'],['#3','2021-01-01']],'run'),
 ('Start date left empty (full history)','(empty)','VEC','Backtest runs from earliest common date',[],'run'),
 ('Start date after end date','2020-01-01 (end 2019-01-01)','IEC',REJ,[['#2','2020-01-01'],['#3','2019-01-01']],'toast'),
 ('Start date equal to end date','2020-01-01 (end 2020-01-01)','IEC',REJ,[['#2','2020-01-01'],['#3','2020-01-01']],'toast'),
 ('Start date earlier than first available data','1990-01-01 (end 2020-01-01)','IEC','Rejected, or user told the start is adjusted',[['#2','1990-01-01'],['#3','2020-01-01']],'run_bad'),
 ('Start date in the far future (no data)','2099-01-01 (end 2100-01-01)','IEC',REJ,[['#2','2099-01-01'],['#3','2100-01-01']],'toast')])
F(BT,'End Date',[
 ('Valid end date with start empty','2020-01-01 (start empty)','VEC','Backtest runs up to the entered date',[['#3','2020-01-01']],'run'),
 ('Start only, end date empty (runs to latest data)','2020-01-01 (end empty)','VEC','Backtest runs to latest data',[['#2','2020-01-01']],'run'),
 ('End date later than last available data','2020-01-01 to 2030-01-01','IEC','Rejected, or user told the end is adjusted',[['#2','2020-01-01'],['#3','2030-01-01']],'run_bad')])
F(BT,'Starting Value',[
 ('Valid starting value (>=1, below upper limit)','10000','VEC',RUN_OK,[['#4','10000']],'run'),
 ('Zero starting value','0','IEC',REJ,[['#4','0']],'native'),
 ('Negative starting value','-5','IEC',REJ,[['#4','-5']],'native'),
 ('Fractional value below minimum','0.5','IEC',REJ,[['#4','0.5']],'native'),
 ('Empty starting value','(empty)','IEC',REJ,[['#4','']],'toast'),
 ('Starting value above the upper limit','5000000000000','IEC',REJ,[['#4','5000000000000']],'toast')])
F(BT,'Rolling Window',[
 ('Valid rolling window in months','60','VEC',RUN_OK,[['#6','60']],'run'),
 ('Zero rolling window','0','IEC',REJ,[['#6','0']],'native'),
 ('Negative rolling window','-1','IEC',REJ,[['#6','-1']],'native'),
 ('Non-integer rolling window','1.5','IEC',REJ,[['#6','1.5']],'native'),
 ('Rolling window above upper limit','20000','IEC',REJ,[['#6','20000']],'toast')])
F(BT,'Annual cashflow growth',[
 ('Valid growth percentage','2','VEC',RUN_OK,[['#10','2']],'run'),
 ('Growth below minimum','-100','IEC',REJ,[['#10','-100']],'native'),
 ('Growth above maximum','101','IEC',REJ,[['#10','101']],'native')])
F(BT,'Cashflow amount',[
 ('Positive cashflow (contribution)','1000','VEC',RUN_OK,[['#12','1000']],'run'),
 ('Negative cashflow (withdrawal)','-500','VEC',RUN_OK,[['#12','-500']],'run'),
 ('Zero cashflow (no cashflow)','0','VEC',RUN_OK,[['#12','0']],'run')])
F(BT,'Drag (annual fee %)',[
 ('Valid drag between 0 and 100','0.5','VEC',RUN_OK,[['#19','0.5']],'run'),
 ('Negative drag','-1','IEC',REJ,[['#19','-1']],'run_bad'),
 ('Drag above 100%','150','IEC',REJ,[['#19','150']],'run_bad')])
F(BT,'Ticker',[
 ('Valid ticker (upper case)','SPY','VEC',RUN_OK,[['#22','SPY']],'run'),
 ('Valid ticker in lower case','spy','VEC',RUN_OK,[['#22','spy']],'run'),
 ('Unknown ticker','ZZZZZZ','IEC',REJ,[['#22','ZZZZZZ']],'toast'),
 ('Empty ticker with non-zero allocation','(empty)','IEC',REJ,[['#22','']],'toast'),
 ('SQL fragment as ticker',"' OR 1=1 --",'IEC',REJ,[['#22',"' OR 1=1 --"]],'toast'),
 ('Non-ASCII (unicode) ticker','ÄÖÜ','IEC',REJ,[['#22','ÄÖÜ']],'toast'),
 ('Ticker containing a space','S PY','IEC',REJ,[['#22','S PY']],'toast'),
 ('Very long ticker (50 characters)','ABCDEFGHIJ x5','IEC',REJ,[['#22','ABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJABCDEFGHIJ']],'toast')])
F(BT,'Allocation % (portfolio total)',[
 ('Allocations sum to exactly 100 across 2 assets','SPY 60 / AGG 40','VEC',RUN_OK,[],'run'),
 ('Single asset at 100%','SPY 100 / AGG 0','VEC',RUN_OK,[['#23','100'],['#25','0']],'run'),
 ('Allocations sum below 100','SPY 60 / AGG 30 (90)','IEC',REJ,[['#25','30']],'toast'),
 ('Allocations sum above 100','SPY 60 / AGG 60 (120)','IEC',REJ,[['#25','60']],'toast'),
 ('Negative allocation with offsetting excess','SPY -10 / AGG 110','IEC',REJ,[['#23','-10'],['#25','110']],'run_bad')])
F(BT,'Rebalance frequency',[
 ('Valid rebalance option (Yearly, default)','Yearly','VEC',RUN_OK,[],'run')])

MC='MC'
F(MC,'Start / End Date',[
 ('Dates empty (full history)','(empty)','VEC','Simulation runs',[],'run'),
 ('Start date after end date','2020-01-01 / 2019-01-01','IEC',REJ,[['Start Date','2020-01-01'],['End Date','2019-01-01']],'toast')])
F(MC,'Number of years',[
 ('Valid horizon within free limit','10','VEC',RUN_OK,[['Number of years','10']],'run'),
 ('Horizon below minimum','0','IEC',REJ,[['Number of years','0']],'native'),
 ('Horizon above free-plan limit but within 100','50','IEC','Rejected or plan-limit message',[['Number of years','50']],'gate'),
 ('Horizon above absolute maximum','150','IEC',REJ,[['Number of years','150']],'native'),
 ('Decimal horizon','2.5','VEC',RUN_OK,[['Number of years','2.5']],'run')])
F(MC,'Starting Value',[
 ('Valid starting value','10000','VEC',RUN_OK,[['Starting Value','10000']],'run'),
 ('Zero starting value','0','IEC',REJ,[['Starting Value','0']],'native')])
F(MC,'Min block (years)',[
 ('Valid minimum block length','1','VEC',RUN_OK,[['Min block','1']],'run'),
 ('Minimum block below allowed minimum','0.01','IEC',REJ,[['Min block','0.01']],'native')])
F(MC,'Max block (years)',[
 ('Valid maximum block length','5','VEC',RUN_OK,[['Max block','5']],'run'),
 ('Maximum block above allowed maximum','25','IEC',REJ,[['Max block','25']],'native'),
 ('Maximum block below allowed minimum','0.01','IEC',REJ,[['Max block','0.01']],'native')])
F(MC,'Random seed',[
 ('Seed left empty (random)','(empty)','VEC',RUN_OK,[],'run'),
 ('Valid whole-number seed','42','VEC',RUN_OK,[['Random seed','42']],'run'),
 ('Negative seed','-1','IEC',REJ,[['Random seed','-1']],'native'),
 ('Non-integer seed','1.5','IEC',REJ,[['Random seed','1.5']],'native')])
F(MC,'Allocation % (portfolio total)',[
 ('Allocations sum to 100 (50/25/25)','50/25/25','VEC',RUN_OK,[],'run'),
 ('Allocations sum below 100','50/25/20 (95)','IEC',REJ,[['#22','20']],'toast')])

SW='SW'
F(SW,'Retirement horizon (years)',[
 ('Valid horizon','30','VEC',RUN_OK,[['#6','30']],'run'),
 ('Zero horizon','0','IEC',REJ,[['#6','0']],'toast'),
 ('Horizon above maximum','60','IEC',REJ,[['#6','60']],'native')])
F(SW,'Phase 1 end year',[
 ('Valid end year before horizon','10','VEC',RUN_OK,[['#7','10']],'run'),
 ('End year zero','0','IEC',REJ,[['#7','0']],'toast'),
 ('End year after the horizon','40 (horizon 30)','IEC',REJ,[['#7','40']],'toast')])
F(SW,'Phase 1 annual withdrawal %',[
 ('Valid withdrawal rate','4','VEC',RUN_OK,[['#8','4']],'run'),
 ('Withdrawal rate negative','-5','IEC',REJ,[['#8','-5']],'native'),
 ('Withdrawal rate above 100','150','IEC',REJ,[['#8','150']],'native')])
F(SW,'Phase 2 annual withdrawal %',[
 ('Valid withdrawal rate','6','VEC',RUN_OK,[['#10','6']],'run'),
 ('Withdrawal rate negative','-5','IEC',REJ,[['#10','-5']],'native'),
 ('Withdrawal rate above 100','150','IEC',REJ,[['#10','150']],'native')])
F(SW,'Start / End Date',[
 ('Dates empty (full history)','(empty)','VEC',RUN_OK,[],'run'),
 ('Start date after end date','2020-01-01 / 2019-01-01','IEC',REJ,[['Start Date','2020-01-01'],['End Date','2019-01-01']],'toast')])
F(SW,'Allocation % (portfolio total)',[
 ('Allocations sum to 100 (50/30/20)','50/30/20','VEC',RUN_OK,[],'run'),
 ('Allocations sum below 100','50/30/10 (90)','IEC',REJ,[['#22','10']],'toast')])

OP='OP'
T3=['Tickers','SPY AGG GLD']
F(OP,'Tickers',[
 ('Three valid tickers separated by spaces','SPY AGG GLD','VEC',RUN_OK,[T3],'run'),
 ('Exactly two valid tickers','SPY AGG','VEC',RUN_OK,[['Tickers','SPY AGG']],'run'),
 ('Only one ticker','SPY','IEC',REJ,[['Tickers','SPY']],'toast'),
 ('Empty tickers','(empty)','IEC',REJ,[['Tickers','']],'toast'),
 ('Contains an unknown ticker','SPY ZZZZZZ','IEC',REJ,[['Tickers','SPY ZZZZZZ']],'toast'),
 ('Comma-separated tickers','SPY,AGG,GLD','IEC',REJ,[['Tickers','SPY,AGG,GLD']],'toast')])
F(OP,'Start / End Date',[
 ('Dates empty (full history)','(empty)','VEC',RUN_OK,[T3],'run'),
 ('Start date after end date','2020-01-01 / 2019-01-01','IEC',REJ,[T3,['Start Date','2020-01-01'],['End Date','2019-01-01']],'toast')])
F(OP,'Starting Value',[
 ('Valid starting value','10000','VEC',RUN_OK,[T3,['Starting Value','10000']],'run'),
 ('Zero starting value','0','IEC',REJ,[T3,['Starting Value','0']],'native')])
F(OP,'Rolling Window',[
 ('Valid rolling window','60','VEC',RUN_OK,[T3,['Rolling Window','60']],'run'),
 ('Zero rolling window','0','IEC',REJ,[T3,['Rolling Window','0']],'native')])
F(OP,'Max holdings',[
 ('Valid max holdings','2','VEC',RUN_OK,[T3,['Max holdings','2']],'run'),
 ('Zero max holdings','0','IEC',REJ,[T3,['Max holdings','0']],'native')])
F(OP,'Min weight to include (%)',[
 ('Valid minimum weight','10','VEC',RUN_OK,[T3,['Min weight to include','10']],'run'),
 ('Negative minimum weight','-5','IEC',REJ,[T3,['Min weight to include','-5']],'native'),
 ('Minimum weight above 100','150','IEC',REJ,[T3,['Min weight to include','150']],'native')])
F(OP,'Max vol (%)',[
 ('Valid maximum volatility','20','VEC',RUN_OK,[T3,['Max vol','20']],'run'),
 ('Negative maximum volatility','-5','IEC',REJ,[T3,['Max vol','-5']],'native')])

EF='EF'
T2=['Tickers','SPY AGG']
F(EF,'Tickers',[
 ('Two valid tickers','SPY AGG','VEC',RUN_OK,[T2],'run'),
 ('Only one ticker','SPY','IEC',REJ,[['Tickers','SPY']],'toast'),
 ('Empty tickers','(empty)','IEC',REJ,[['Tickers','']],'toast'),
 ('Three tickers (above free-plan limit)','SPY AGG GLD','IEC','Rejected or plan-limit message',[['Tickers','SPY AGG GLD']],'gate')])
F(EF,'Start / End Date',[
 ('Dates empty (full history)','(empty)','VEC',RUN_OK,[T2],'run'),
 ('Start date after end date','2020-01-01 / 2019-01-01','IEC',REJ,[T2,['Start Date','2020-01-01'],['End Date','2019-01-01']],'toast')])
F(EF,'Max holdings',[
 ('Valid max holdings','2','VEC',RUN_OK,[T2,['Max holdings','2']],'run'),
 ('Zero max holdings','0','IEC',REJ,[T2,['Max holdings','0']],'native')])
F(EF,'Min weight to include (%)',[
 ('Valid minimum weight','10','VEC',RUN_OK,[T2,['Min weight to include','10']],'run'),
 ('Negative minimum weight','-5','IEC',REJ,[T2,['Min weight to include','-5']],'native'),
 ('Minimum weight above 100','150','IEC',REJ,[T2,['Min weight to include','150']],'native')])

LD='LD'
LDB=[['#15','SPY'],['#16','60'],['#17','AGG'],['#18','40']]
F(LD,'Starting Value',[
 ('Valid starting value (>=100)','10000','VEC',GATE_OK,LDB+[['Starting Value','10000']],'gate'),
 ('Starting value below minimum','50','IEC',REJ,LDB+[['Starting Value','50']],'native')])
F(LD,'DCA horizon (months)',[
 ('Valid horizon','12','VEC',GATE_OK,LDB+[['DCA horizon','12']],'gate'),
 ('Horizon below minimum','0','IEC',REJ,LDB+[['DCA horizon','0']],'native'),
 ('Horizon above maximum','200','IEC',REJ,LDB+[['DCA horizon','200']],'native')])
F(LD,'Ticker',[
 ('Valid ticker','SPY','VEC',GATE_OK,LDB,'gate'),
 ('Unknown ticker','ZZZZZZ','IEC','Validation message shown',[['#15','ZZZZZZ'],['#16','60'],['#17','AGG'],['#18','40']],'gate')])
F(LD,'Allocation % (portfolio total)',[
 ('Allocations sum to 100','60/40','VEC',GATE_OK,LDB,'gate'),
 ('Allocations sum below 100','60/30 (90)','IEC','Validation message shown',[['#15','SPY'],['#16','60'],['#17','AGG'],['#18','30']],'gate')])

TV='TV'
F(TV,'Starting Value',[
 ('Valid starting value','10000','VEC',RUN_OK,[['Starting Value','10000']],'run'),
 ('Negative starting value','-500','IEC',REJ,[['Starting Value','-500']],'toast'),
 ('Starting value above maximum','9000000','IEC',REJ,[['Starting Value','9000000']],'toast'),
 ('Empty starting value','(empty)','IEC',REJ,[['Starting Value','']],'toast')])
F(TV,'Monthly contribution',[
 ('Valid monthly contribution','1000','VEC',RUN_OK,[['Monthly contribution','1000']],'run'),
 ('Negative contribution','-50','IEC',REJ,[['Monthly contribution','-50']],'toast'),
 ('Contribution above maximum','500000','IEC',REJ,[['Monthly contribution','500000']],'toast')])

RB='RB'
RBB=[['#13','SPY'],['#14','60'],['#15','AGG'],['#16','40']]
F(RB,'Start / End Date',[
 ('Dates empty (full history)','(empty)','VEC',GATE_OK,RBB,'gate'),
 ('Start date after end date','2020-01-01 / 2019-01-01','IEC','Validation message shown',RBB+[['Start Date','2020-01-01'],['End Date','2019-01-01']],'gate')])
F(RB,'Drag (annual fee %)',[
 ('Valid drag','0.5','VEC',GATE_OK,RBB+[['#11','0.5']],'gate'),
 ('Negative drag','-2','IEC','Validation message shown',RBB+[['#11','-2']],'gate')])
F(RB,'Allocation % (portfolio total)',[
 ('Allocations sum to 100','60/40','VEC',GATE_OK,RBB,'gate'),
 ('Allocations sum below 100','60/30 (90)','IEC','Validation message shown',[['#13','SPY'],['#14','60'],['#15','AGG'],['#16','30']],'gate')])

STRONG = [
 ('Strong EP 1: every field in a valid class simultaneously','Start 2015-01-01, End 2020-01-01, SV 50000, RW 36, growth 2, cashflow 100, drag 0.5, SPY60/AGG40',RUN_OK,[['#2','2015-01-01'],['#3','2020-01-01'],['#4','50000'],['#6','36'],['#10','2'],['#12','100'],['#19','0.5']],'run'),
 ('Strong EP 2: three numeric fields invalid simultaneously','SV 0, RW 0, growth -100','All three invalid fields are flagged; no run',[['#4','0'],['#6','0'],['#10','-100']],'native'),
 ('Strong EP 3: valid numerics + unknown ticker + allocation sum 90','ticker ZZZZZZ, alloc 60/30','Both problems are reported; no run',[['#22','ZZZZZZ'],['#25','30']],'toast'),
 ('Strong EP 4: invalid date order + empty starting value + unknown ticker + alloc sum 120','2020-01-01/2019-01-01, SV empty, ZZZZZZ, 60/60','All problems are reported; no run',[['#2','2020-01-01'],['#3','2019-01-01'],['#4',''],['#22','ZZZZZZ'],['#25','60']],'toast'),
 ('Strong EP 5: valid dates + valid numerics + negative allocation (invalid)','2015-01-01/2020-01-01, SV 50000, alloc -10/110',REJ,[['#2','2015-01-01'],['#3','2020-01-01'],['#4','50000'],['#23','-10'],['#25','110']],'run_bad'),
 ('Strong EP 6: empty ticker + drag above 100','ticker empty, drag 150','Both problems are reported; no run',[['#22',''],['#19','150']],'toast'),
]
