# ArcGIS_Describe_Geodatabase
Python toolbox for describing the structure of an ArcGIS geodatabase

## Purpose: Write geodatabase strucutural details to file.

    Will create a unique .csv table for each table or feature class in a database detailing:
        *name
        *aliasName
        *type
        *length
        *precision
        *scale
        *defaultValue
        *domain
        *editable
        *isNullable
        *required
        *unique records
        
    Will create a unique csv for each domain
    
    Will create a csv detailing all the relationship classes in a database:
        *originClassName
        *originClassKey
        *destinationClassName
        *destinationClassKey
        *forwardPathLabel
        *backwardPathLabel
        *cardinality
        *classKey
        *keyType
        *isAttributed
        *isComposite
        *isReflexive
        *notification
