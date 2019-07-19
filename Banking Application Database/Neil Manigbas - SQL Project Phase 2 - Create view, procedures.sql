USE Bank;
-------------------------------------------
--1.	Create a view to get all customers with checking account from ON province. 
CREATE VIEW V_ON_Checking
AS

SELECT CustomerFirstName 'First Name', CustomerLastName 'Last Name', City, State, C.AccountID, AccountTypeDescription 'Account Description'
FROM Customer C
JOIN Account A
ON C.AccountID = A.AccountID
JOIN AccountType AT
ON A.AccountTypeID = AT.AccountTypeID
WHERE State = 'ON'
AND AccountTypeDescription = 'Cheque';

SELECT * FROM V_ON_Checking;
--select * from AccountType;
--select * from Account;

-------------------------------------------
--2.	Create a view to get all customers with total account balance (including interest rate) greater than 5000. 
CREATE VIEW V_BAL_GRTR_5000
AS

SELECT CustomerFirstName 'First Name', CustomerLastName 'Last Name', C.AccountID, convert(decimal(15,2), CurrentBalance * (1 + (InterestRateValue))) 'Balance After Rate'
FROM Customer C
JOIN Account A
ON C.AccountID = A.AccountID
JOIN SavingsInterestRates R
ON A.InterestSavingsRateID = R.InterestSavingsRateID
WHERE CurrentBalance * (1 + InterestRateValue) > 5000;

SELECT * FROM V_BAL_GRTR_5000;
--select * from Account;
--select * from SavingsInterestRates;

-------------------------------------------
--3.	Create a view to get counts of checking and savings accounts by customer.
CREATE VIEW V_Count_Chq_Sav
AS

SELECT CustomerID, CustomerFirstName 'First Name', CustomerLastName 'Last Name', C.AccountID, COUNT(ATC.AccountTypeDescription)'Chq Accounts', COUNT(ATS.AccountTypeDescription)'Sav Accounts'
FROM Customer C
LEFT JOIN Account A
ON C.AccountID = A.AccountID
LEFT JOIN 
(
	SELECT *
	FROM AccountType 
	WHERE AccountTypeDescription = 'Cheque'
)	ATC
ON A.AccountTypeID = ATC.AccountTypeID
LEFT JOIN 
(
	SELECT *
	FROM AccountType 
	WHERE AccountTypeDescription = 'Savings'
)	ATS
ON A.AccountTypeID = ATS.AccountTypeID
GROUP BY CustomerID, CustomerFirstName, CustomerLastName, C.AccountID;

SELECT * FROM V_Count_Chq_Sav;

--------------------------------------------
--4.	Create a view to get any particular user’s login and password using AccountId. 
CREATE VIEW V_Login_w_AcctID
AS

SELECT AccountID, UserLogin Username, UserPassword Password
FROM UserLogins U
JOIN [Login-Account] LA
ON U.UserLoginID = LA.UserLoginID;

SELECT * FROM V_Login_w_AcctID;
--select * from UserLogins;
--select * from [Login-Account];

----------------------------------------------
--5.	Create a view to get all customers’ overdraft amount. 
CREATE VIEW V_Overdraft
AS

SELECT CustomerID, CustomerFirstName, CustomerLastName, C.AccountID, SUM(OverDraftAmount) 'Overdraft SUM'
FROM Customer C
JOIN OverDraftLog O
ON C.AccountID = O.AccountID
GROUP BY CustomerID, CustomerFirstName, CustomerLastName, C.AccountID;

SELECT * FROM V_Overdraft;
--select * from OverDaftLog;

------------------------------------------------
--6.	Create a stored procedure to add “User_” as a prefix to everyone’s login (username). 
CREATE PROCEDURE P_add_text_User
AS
BEGIN
	BEGIN TRANSACTION
		UPDATE UserLogins
		SET UserLogin = 'User_' + UserLogin

END;

EXECUTE P_add_text_User;
--rollback;

-----------------------------------------------
--7.	Create a stored procedure that accepts AccountId as a parameter and returns customer’s full name. 
CREATE PROCEDURE P_AcctID_for_Name
@AccountID smallint
AS
BEGIN
	SELECT CustomerFirstName FirstName, CustomerLastName LastName
	FROM Customer
	WHERE AccountID = @AccountID
END;

--select * from Customer;
EXECUTE P_AcctID_for_Name 1001;

-------------------------------------------------
--8.	Create a stored procedure that takes a deposit as a parameter and updates CurrentBalance value for that particular account.
CREATE PROCEDURE P_Deposit_update_Bal
@Deposit int,
@AccountID smallint
AS
BEGIN
	--BEGIN TRANSACTION
		UPDATE Account
		SET CurrentBalance = CurrentBalance + @Deposit
		WHERE AccountID = @AccountID
END;

EXECUTE P_Deposit_update_Bal 500/*Deposit*/, 1001/*AccountID*/;
--select * from Account;

-------------------------------------------
--9.	Create a stored procedure that takes a withdrawal amount as a parameter and updates CurrentBalance value for that particular account. 
CREATE PROCEDURE P_withdraw_update_Bal
@Withdraw int,
@AccountID smallint
AS
BEGIN
	--BEGIN TRANSACTION
		UPDATE Account
		SET CurrentBalance = CurrentBalance - @Withdraw
		WHERE AccountID = @AccountID
END;

EXECUTE P_withdraw_update_Bal 500/*Withdrawal*/, 1001/*AccountID*/;
--select * from Account;

----------------------------------------------
--10.	Write a query to remove SSN column from Customer table. 
--begin transaction
ALTER TABLE Customer
DROP COLUMN SSN;
--rollback
--select * from Customer