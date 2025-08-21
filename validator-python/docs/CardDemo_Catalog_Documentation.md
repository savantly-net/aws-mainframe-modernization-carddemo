# CardDemo Application Catalog Documentation

## Overview

This document provides a comprehensive overview of the CardDemo application catalog, which is a complete inventory of all datasets, VSAM files, and system components that make up the CardDemo credit card management application.

## What is the Catalog?

The catalog is a **VSAM catalog listing** generated using IBM's IDCAMS (Access Method Services) utility. It serves as a complete inventory of all data assets within the CardDemo application, providing detailed information about:

- **Dataset names and types**
- **Storage characteristics** (space allocation, volumes, extents)
- **Performance statistics** (record counts, I/O operations)
- **Security settings** (RACF protection, encryption)
- **Data relationships** (VSAM clusters, indexes, alternate indexes)
- **System management** (SMS classes, backup information)

## How the Catalog Was Created

The catalog listing was generated using the following JCL job (`samples/jcl/LISTCAT.jcl`):

```jcl
//STEP05 EXEC PGM=IDCAMS,COND=(0,NE)
//SYSPRINT DD   DISP=(NEW,CATLG,DELETE),
//         UNIT=SYSDA,
//         DCB=(RECFM=FBA,LRECL=133,BLKSIZE=0),
//         SPACE=(TRK,(1,1)),
//         DSN=AWS.M2.CARDDEMO.LISTCAT
//SYSIN    DD   *
   LISTCAT LEVEL(AWS.M2.CARDDEMO)  -
           ALL
/*
```

### Command Breakdown:

- **`LISTCAT`**: IDCAMS command to list catalog entries
- **`LEVEL(AWS.M2.CARDDEMO)`**: Lists all datasets with this high-level qualifier
- **`ALL`**: Includes all detailed information (attributes, statistics, associations)

## Catalog Summary

The catalog contains **209 total entries** across the following categories:

| Entry Type  | Count | Description                                              |
| ----------- | ----- | -------------------------------------------------------- |
| **NONVSAM** | 160   | Sequential files, libraries, and other non-VSAM datasets |
| **CLUSTER** | 10    | VSAM Key Sequenced Data Sets (KSDS)                      |
| **DATA**    | 13    | VSAM data components                                     |
| **INDEX**   | 13    | VSAM index components                                    |
| **GDG**     | 7     | Generation Data Groups                                   |
| **AIX**     | 3     | Alternate Indexes                                        |
| **PATH**    | 3     | VSAM paths for alternate indexes                         |

## Key Application Datasets

### Core Business Data

#### Account Management

- **`AWS.M2.CARDDEMO.ACCTDATA.PS`** - Sequential account data file
- **`AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS`** - VSAM account data with indexes
- **`AWS.M2.CARDDEMO.ACCTDATA.VSAM.AIX`** - Alternate index for account lookups

#### Customer Management

- **`AWS.M2.CARDDEMO.CUSTDATA.PS`** - Sequential customer data file
- **`AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS`** - VSAM customer data with indexes

#### Credit Card Management

- **`AWS.M2.CARDDEMO.CARDDATA.PS`** - Sequential card data file
- **`AWS.M2.CARDDEMO.CARDDATA.VSAM.KSDS`** - VSAM card data with indexes
- **`AWS.M2.CARDDEMO.CARDDATA.VSAM.AIX`** - Alternate index for card lookups
- **`AWS.M2.CARDDEMO.CARDXREF.PS`** - Sequential card cross-reference file
- **`AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS`** - VSAM card cross-reference with indexes

#### Transaction Processing

- **`AWS.M2.CARDDEMO.DALYTRAN.PS`** - Daily transaction file
- **`AWS.M2.CARDDEMO.DALYTRAN.PS.INIT`** - Initial daily transaction data
- **`AWS.M2.CARDDEMO.TCATBALF.PS`** - Transaction category balance file
- **`AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS`** - VSAM transaction category balances

#### Reference Data

- **`AWS.M2.CARDDEMO.DISCGRP.PS`** - Discount group reference data
- **`AWS.M2.CARDDEMO.DISCGRP.VSAM.KSDS`** - VSAM discount group data
- **`AWS.M2.CARDDEMO.TRANCATG.PS`** - Transaction category reference data
- **`AWS.M2.CARDDEMO.TRANCATG.VSAM.KSDS`** - VSAM transaction category data

#### Security

- **`AWS.M2.CARDDEMO.SECURITY.PS`** - Security configuration data
- **`AWS.M2.CARDDEMO.USRSEC.VSAM.KSDS`** - VSAM user security data

### Generation Data Groups (GDGs)

The application uses several GDGs for data management:

#### Transaction Processing

- **`AWS.M2.CARDDEMO.SYSTRAN`** - System transaction backups (5 generations)
- **`AWS.M2.CARDDEMO.TRANSACT.BKUP`** - Transaction backup files (5 generations)
- **`AWS.M2.CARDDEMO.TRANREPT`** - Transaction reports (5 generations)

#### Daily Processing

- **`AWS.M2.CARDDEMO.DALYREJS`** - Daily rejected transactions (5 generations)
- **`AWS.M2.CARDDEMO.TCATBALF.BKUP`** - Transaction category balance backups (5 generations)

### Application Libraries

#### Source Code and Control

- **`AWS.M2.CARDDEMO.CBL`** - COBOL source code
- **`AWS.M2.CARDDEMO.CPY`** - COBOL copybooks
- **`AWS.M2.CARDDEMO.BMS`** - BMS (Basic Mapping Support) definitions
- **`AWS.M2.CARDDEMO.DCL`** - Data Control Language definitions
- **`AWS.M2.CARDDEMO.CNTL`** - Control cards and parameters
- **`AWS.M2.CARDDEMO.JCL`** - JCL job streams
- **`AWS.M2.CARDDEMO.PROC`** - JCL procedures

#### Load Libraries

- **`AWS.M2.CARDDEMO.LOADLIB`** - Compiled program load modules
- **`AWS.M2.CARDDEMO.LISTING`** - Compilation listings
- **`AWS.M2.CARDDEMO.LST`** - Additional listings

#### Utilities

- **`AWS.M2.CARDDEMO.JCL.UTIL`** - Utility JCL jobs
- **`AWS.M2.CARDDEMO.PRC.UTIL`** - Utility procedures
- **`AWS.M2.CARDDEMO.REXX.UTIL`** - REXX utility scripts

## VSAM Structure Details

### VSAM Cluster Components

Each VSAM KSDS (Key Sequenced Data Set) consists of:

1. **CLUSTER** - The main VSAM cluster definition
2. **DATA** - The actual data records
3. **INDEX** - The primary index for key-based access
4. **AIX** (Optional) - Alternate indexes for different access patterns
5. **PATH** (Optional) - Paths to access data through alternate indexes

### Key Characteristics

#### Data Component Attributes

- **Key Length**: Varies by dataset (8-17 bytes)
- **Record Length**: 50-500 bytes depending on data type
- **Control Interval Size**: 8KB-18KB
- **Control Area Size**: 45-90 control intervals per control area

#### Index Component Attributes

- **Key Length**: Same as data component
- **Control Interval Size**: 512 bytes
- **Index Levels**: Single level for all datasets
- **Entries per Section**: 6-9 entries

### Performance Statistics

The catalog shows current usage statistics for each dataset:

- **Record counts** (total, inserted, updated, deleted, retrieved)
- **I/O operations** (EXCPs)
- **Space utilization** (free space percentages)
- **Split operations** (CI and CA splits)

## Storage Management

### SMS (Storage Management Subsystem)

Most datasets use SMS with:

- **Storage Class**: SCTECH
- **Management Class**: NULL (default)
- **Data Class**: NULL (default)

### Volume Distribution

Datasets are distributed across multiple volumes:

- **YYYYTU, YYYYO7, YYYYTO, YYYYTA, YYYYTC** - Primary data volumes
- **YYYYIX, YYYYT0, YYYYO8, YYYYT1** - Library and utility volumes

### Space Allocation

- **Primary Space**: 1-5 cylinders depending on dataset size
- **Secondary Space**: 1-5 cylinders for extensions
- **Space Type**: Cylinder allocation for data, track allocation for indexes

## Security and Protection

### RACF Integration

- **RACF Protection**: NO (not RACF protected)
- **Password Protection**: NULL (no password protection)
- **Data Encryption**: NO (not encrypted)

### Access Control

- **Share Options**: (2,3) for most datasets (cross-region sharing)
- **Recovery**: Enabled for all VSAM datasets
- **Write Check**: Disabled (NOWRITECHK)

## Purpose and Benefits

### Application Management

1. **Complete Inventory**: Provides a comprehensive view of all application assets
2. **Capacity Planning**: Shows space utilization and growth patterns
3. **Performance Analysis**: Reveals I/O patterns and optimization opportunities
4. **Migration Planning**: Essential for understanding data dependencies

### Modernization Support

1. **Discovery**: Identifies all data sources for analysis tools
2. **Assessment**: Helps evaluate data complexity and migration effort
3. **Mapping**: Documents relationships between datasets
4. **Validation**: Provides baseline for migration verification

### Operational Benefits

1. **Troubleshooting**: Quick identification of dataset issues
2. **Backup Planning**: Understanding of data volumes and relationships
3. **Maintenance**: Tracking of dataset changes and growth
4. **Documentation**: Self-documenting data architecture

## Usage Guidelines

### For System Administrators

- Use the catalog to monitor dataset growth and performance
- Plan storage capacity based on current utilization
- Identify datasets requiring attention or optimization

### For Application Developers

- Understand data relationships for program design
- Identify appropriate datasets for new functionality
- Plan data access patterns based on existing indexes

### For Migration Teams

- Use as input for discovery and assessment tools
- Map data dependencies for migration planning
- Validate migration completeness against catalog entries

## Maintenance

### Regular Updates

The catalog should be refreshed periodically to:

- Track dataset growth and changes
- Monitor performance trends
- Update documentation for new datasets

### Refresh Process

1. Run the LISTCAT JCL job
2. Compare with previous catalog listing
3. Document any changes or new datasets
4. Update application documentation

## Conclusion

The CardDemo catalog provides a comprehensive view of the application's data architecture, serving as both documentation and a management tool. It supports various use cases from daily operations to major modernization initiatives, making it an essential component of the CardDemo application ecosystem.

---

_Generated from IDCAMS LISTCAT output on 2022-09-01_
_Total Entries: 209_
_Application: CardDemo v1.0_
