CREATE TABLE DimDate (
    DateKey INT PRIMARY KEY,
    [Date] DATE NOT NULL,
    [Year] INT NOT NULL,
    Quarter NVARCHAR(10) NOT NULL,
    MonthNumber INT NOT NULL,
    MonthName NVARCHAR(20) NOT NULL,
    WeekNumber INT NOT NULL,
    DayOfMonth INT NOT NULL,
    DayOfWeek NVARCHAR(20) NOT NULL,
    IsWeekend BIT NOT NULL
);

CREATE TABLE DimDepartment (
    DepartmentKey INT PRIMARY KEY,
    DepartmentName NVARCHAR(100) NOT NULL,
    RiskTier NVARCHAR(20) NOT NULL,
    ExecutiveOwner NVARCHAR(100) NOT NULL
);

CREATE TABLE DimWorkload (
    WorkloadKey INT PRIMARY KEY,
    WorkloadName NVARCHAR(100) NOT NULL,
    PlatformDomain NVARCHAR(100) NOT NULL,
    PrimaryPersona NVARCHAR(100) NOT NULL
);

CREATE TABLE FactSecurityGovernanceDaily (
    DateKey INT NOT NULL,
    DepartmentKey INT NOT NULL,
    WorkloadKey INT NOT NULL,
    SignInFailures INT NOT NULL,
    HighSeverityIncidents INT NOT NULL,
    MediumSeverityIncidents INT NOT NULL,
    PrivilegedRoleChanges INT NOT NULL,
    GuestAccountsActive INT NOT NULL,
    TeamsCreated INT NOT NULL,
    TeamsArchived INT NOT NULL,
    ComplianceScore DECIMAL(5,2) NOT NULL,
    RiskyDevices INT NOT NULL,
    DataLossEvents INT NOT NULL,
    CONSTRAINT PK_FactSecurityGovernanceDaily
        PRIMARY KEY (DateKey, DepartmentKey, WorkloadKey),
    CONSTRAINT FK_Fact_Date
        FOREIGN KEY (DateKey) REFERENCES DimDate (DateKey),
    CONSTRAINT FK_Fact_Department
        FOREIGN KEY (DepartmentKey) REFERENCES DimDepartment (DepartmentKey),
    CONSTRAINT FK_Fact_Workload
        FOREIGN KEY (WorkloadKey) REFERENCES DimWorkload (WorkloadKey)
);
