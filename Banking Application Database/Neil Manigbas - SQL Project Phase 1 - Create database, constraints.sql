DROP DATABASE Bank;

CREATE DATABASE Bank;

USE Bank;

CREATE TABLE UserLogins
(
	UserLoginID smallint PRIMARY KEY,
	UserLogin char(30) NOT NULL,--changed number of char from 15 to accomodate item no. 6 in Phase 2
	UserPassword varchar(20) NOT NULL
);

CREATE TABLE UserSecurityQuestions
(
	UserSecurityQuestionsID tinyint PRIMARY KEY,
	UserSecurityQuestion varchar(50)
);

CREATE TABLE AccountType
(
	AccountTypeID tinyint PRIMARY KEY,
	AccountTypeDescription varchar(30)
);

CREATE TABLE SavingsInterestRates
(
	InterestSavingsRateID tinyint PRIMARY KEY,
	InterestRateValue numeric(30,9) NOT NULL,--modified numeric value from (9,9) due to 'overflow' error when inserting records
	InterestRateDescription varchar(20)
);

CREATE TABLE AccountStatusType
(
	AccountStatusTypeID tinyint PRIMARY KEY,
	AccountStatusDescription varchar(30)
);

CREATE TABLE Employee
(
	EmployeeID int PRIMARY KEY,
	EmployeeFirstName varchar(25) NOT NULL,
	EmployeeMiddleInitial char(1),
	EmployeeLastName varchar(25) NOT NULL,
	EmployeesManager bit
);

CREATE TABLE TransactionType
(
	TransactionTypeID tinyint PRIMARY KEY,
	TransactionTypeName char(10) NOT NULL,
	TransactionTypeDescription varchar(50),
	TransactionFeeAmount smallmoney
);

CREATE TABLE LoginErrorLog
(
	ErrorLogID int PRIMARY KEY,
	Errortime datetime,
	FailedTransactionXML xml
);

CREATE TABLE FailedTransactionErrorType
(
	FailedTransactionErrorTypeID tinyint PRIMARY KEY,
	FailedTransactionDescription varchar(50)
);

CREATE TABLE Account
(
	AccountID int PRIMARY KEY,
	CurrentBalance int NOT NULL,
	AccountTypeID tinyint FOREIGN KEY REFERENCES AccountType(AccountTypeID),
	AccountStatusTypeID tinyint FOREIGN KEY REFERENCES AccountStatusType(AccountStatusTypeID),
	InterestSavingsRateID tinyint FOREIGN KEY REFERENCES SavingsInterestRates(InterestSavingsRateID)
);

CREATE TABLE [Login-Account]
(
	UserLoginID smallint FOREIGN KEY REFERENCES UserLogins(UserLoginID),
	AccountID int FOREIGN KEY REFERENCES Account(AccountID)
);

CREATE TABLE UserSecurityAnswers
(
	UserLoginID smallint FOREIGN KEY REFERENCES UserLogins(UserLoginID),
	UserSecurityAnswer varchar(25) NOT NULL,
	UserSecurityQuestionID tinyint FOREIGN KEY REFERENCES UserSecurityQuestions(UserSecurityQuestionsID)
);

CREATE TABLE OverDraftLog
(
	AccountID int FOREIGN KEY REFERENCES Account(AccountID),
	OverDraftDate datetime,
	OverDraftAmount money,
	OverDraftTransactionXML xml
);

CREATE TABLE Customer
(
	CustomerID int PRIMARY KEY,
	AccountID int FOREIGN KEY REFERENCES Account(AccountID),
	CustomerAddress1 varchar(30) NOT NULL,
	CustomerAddress2 varchar(30),
	CustomerFirstName varchar(30) NOT NULL,
	CustomerMiddleInitial char (1),
	CustomerLastName varchar(30) NOT NULL,
	City varchar(20) NOT NULL,
	State char(2) NOT NULL,
	ZipCode char(10) NOT NULL,
	EmailAddress varchar (40),
	HomePhone char(12),
	CellPhone char (12),
	WorkPhone char (12),
	SSN char(9),
	UserLoginID smallint FOREIGN KEY REFERENCES UserLogins(UserLoginID)
);

CREATE TABLE [Customer-Account]
(
	AccountID int FOREIGN KEY REFERENCES Account(AccountID),
	CustomerID int FOREIGN KEY REFERENCES Customer(CustomerID)
);

CREATE TABLE TransactionLog
(
	TransactionID int PRIMARY KEY,
	TransactionDate datetime,
	TransactionTypeID tinyint FOREIGN KEY REFERENCES TransactionType(TransactionTypeID),
	TransactionAmount money,
	NewBalance money,
	AccountID int FOREIGN KEY REFERENCES Account(AccountID),
	CustomerID int FOREIGN KEY REFERENCES Customer(CustomerID),
	EmployeeID int FOREIGN KEY REFERENCES Employee(EmployeeID),
	UserLoginID smallint FOREIGN KEY REFERENCES UserLogins(UserLoginID)
);

CREATE TABLE FailedTransactionLog
(
	FailedTransactionID int PRIMARY KEY,
	FailedTransactionErrorTypeID tinyint FOREIGN KEY REFERENCES FailedTransactionErrorType(FailedTransactionErrorTypeID),
	FailedTransactionErrorTime datetime,
	FailedTransactionXML xml
);

INSERT INTO UserLogins VALUES (1, 'neilmanigbas', 'Password1');
INSERT INTO UserLogins VALUES (2, 'seflaqui', 'Password2');
INSERT INTO UserLogins VALUES (3, 'user3', 'Password3');
INSERT INTO UserLogins VALUES (4, 'user4', 'Password4');

INSERT INTO UserSecurityQuestions VALUES (1, 'What is the name of your first wife?');
INSERT INTO UserSecurityQuestions VALUES (2, 'What is the name of your first husband?');
INSERT INTO UserSecurityQuestions VALUES (3, 'What is the name of your second wife?');
INSERT INTO UserSecurityQuestions VALUES (4, 'What is the name of your second husband?');

INSERT INTO AccountType VALUES (1, 'Checking');
INSERT INTO AccountType VALUES (2, 'Savings');
INSERT INTO AccountType VALUES (3, 'Loan');
INSERT INTO AccountType VALUES (4, 'Line of Credit');

INSERT INTO SavingsInterestRates VALUES (1, 0.5, 'Lowest Interest');
INSERT INTO SavingsInterestRates VALUES (2, 1.5, 'Minimum Interest');
INSERT INTO SavingsInterestRates VALUES (3, 2.5, 'Moderate Interest');
INSERT INTO SavingsInterestRates VALUES (4, 3.5, 'Maximum Interest');

INSERT INTO AccountStatusType VALUES (1, 'Active');
INSERT INTO AccountStatusType VALUES (2, 'Inactive');
INSERT INTO AccountStatusType VALUES (3, 'Pending');
INSERT INTO AccountStatusType VALUES (4, 'Cancelled');

INSERT INTO Employee VALUES (1, 'Nimfa', '', 'Manigbas', NULL);
INSERT INTO Employee VALUES (2, 'Jun', '', 'Marcial', 1);
INSERT INTO Employee VALUES (4, 'Matt', '', 'Vincent', 1);
INSERT INTO Employee VALUES (3, 'Gian', '', 'Carlo', 1);
INSERT INTO Employee VALUES (5, 'Kim', '', 'Berly', 1);

INSERT INTO TransactionType VALUES (1, 'Withdraw', 'Account Balance minus Withdrawal', $2.10);
INSERT INTO TransactionType VALUES (2, 'Deposit', 'Account Balance plus Withdrawal', $1.10);
INSERT INTO TransactionType VALUES (3, 'Transfer', 'Account Balance transfers to another Account', $1.00);
INSERT INTO TransactionType VALUES (4, 'Borrow', 'Take on a Loan', $5.10);

INSERT INTO LoginErrorLog VALUES (1, '2018-10-26 01:02:03', '');
INSERT INTO LoginErrorLog VALUES (2, '2018-11-26 04:05:06', '');
INSERT INTO LoginErrorLog VALUES (3, '2018-04-15 09:08:07', '');
INSERT INTO LoginErrorLog VALUES (4, '2018-10-04 10:11:12', '');

INSERT INTO FailedTransactionErrorType VALUES (1, 'Transaction Error 1');
INSERT INTO FailedTransactionErrorType VALUES (2, 'Transaction Error 2');
INSERT INTO FailedTransactionErrorType VALUES (3, 'Transaction Error 3');
INSERT INTO FailedTransactionErrorType VALUES (4, 'Transaction Error 4');

INSERT INTO Account VALUES (1001, 4500, 4, 1, 2);
INSERT INTO Account VALUES (2002, 9000, 3, 2, 4);
INSERT INTO Account VALUES (3003, 3500, 2, 3, 1);
INSERT INTO Account VALUES (4004, 7000, 1, 4, 3);

INSERT INTO [Login-Account] VALUES (1, 1001);
INSERT INTO [Login-Account] VALUES (2, 2002);
INSERT INTO [Login-Account] VALUES (3, 3003);
INSERT INTO [Login-Account] VALUES (4, 4004);

INSERT INTO UserSecurityAnswers VALUES (1, 'Seffy', 1);
INSERT INTO UserSecurityAnswers VALUES (2, 'Neil', 2);
INSERT INTO UserSecurityAnswers VALUES (3, 'Steph', 3);
INSERT INTO UserSecurityAnswers VALUES (4, 'Thor', 4);

INSERT INTO OverDraftLog VALUES (1001, '2018-10-26 01:02:03', 0, '');
INSERT INTO OverDraftLog VALUES (2002, '2018-11-26 04:05:06', 0, '');
INSERT INTO OverDraftLog VALUES (3003, '2018-04-15 09:08:07', 40, '');
INSERT INTO OverDraftLog VALUES (4004, '2018-10-04 10:11:12', 400, '');

INSERT INTO Customer VALUES (1, 1001, 'Keele St', '', 'Neil', '', 'Manigbas', 'North York', 'ON', 'M6M', 'neilchristianmanigbas@gmail.com', '', '647-701-1260', '', '1234', 1);
INSERT INTO Customer VALUES (2, 2002, 'Keele St', '', 'Sef', '', 'Laqui', 'North York', 'ON', 'M6M', 'seflaqui@ymail.com', '', '647-771-1267', '', '3486', 2);
INSERT INTO Customer VALUES (3, 3003, 'Eglinton Ave East', '', 'Zasha', '', 'Aira', 'Scarborough', 'ON', 'M1J', 'ethan@yahoo.com', '', '416-701-1260', '', '58222', 3);
INSERT INTO Customer VALUES (4, 4004, 'Don Mills Rd', '', 'Lott', '', 'Omaxx', 'Toronto', 'ON', 'M3C', 'olg@gmail.com', '', '416-771-1267', '', '45661', 4);

INSERT INTO [Customer-Account] VALUES (1001, 1);
INSERT INTO [Customer-Account] VALUES (2002, 1);
INSERT INTO [Customer-Account] VALUES (3003, 2);
INSERT INTO [Customer-Account] VALUES (4004, 3);

INSERT INTO TransactionLog VALUES (1, '2018-10-26 01:02:03', 1, 500, 4000, 1001, 1, 1, 1);
INSERT INTO TransactionLog VALUES (2, '2018-11-26 04:05:06', 2, 1500, 105000, 2002, 2, 2, 2);
INSERT INTO TransactionLog VALUES (3, '2018-04-15 09:08:07', 1, 300, 3200, 3003, 3, 3, 3);
INSERT INTO TransactionLog VALUES (4, '2018-10-04 10:11:12', 2, 2000, 9000, 4004, 4, 4, 4);

INSERT INTO FailedTransactionLog VALUES (1, 4, '2018-10-26 01:02:03', '');
INSERT INTO FailedTransactionLog VALUES (2, 2, '2018-11-26 04:05:06', '');
INSERT INTO FailedTransactionLog VALUES (3, 1, '2018-04-15 09:08:07', '');
INSERT INTO FailedTransactionLog VALUES (4, 3, '2018-10-04 10:11:12', '');
