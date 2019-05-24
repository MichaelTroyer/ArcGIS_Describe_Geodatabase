# ArcGIS Describe Geodatabase
Python toolbox for describing the structure of an ArcGIS geodatabase

## Purpose: Write geodatabase strucutural details to file.

    Will create a unique .csv table for each table or feature class in a database detailing for each field:
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
        *unique record count
        
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
