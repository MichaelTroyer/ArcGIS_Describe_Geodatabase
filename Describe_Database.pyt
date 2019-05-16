# -*- coding: utf-8 -*-

"""
Author:
Michael Troyer

Date:
12/19/2017

Purpose:
Write geodatabase details to file.

    Will create a unique .csv table for each table or feature class in a database detailing:
        * name
        * aliasName
        * type
        * length
        * precision
        * scale
        * defaultValue
        * domain
        * editable
        * isNullable
        * required
        * unique records

    Will create a unique csv for each domain

    Will create a csv detailing all the relationship classes in a database:
        * originClassName
        * originClassKey
        * destinationClassName
        * destinationClassKey
        * forwardPathLabel
        * backwardPathLabel
        * cardinality
        * classKey
        * keyType
        * isAttributed
        * isComposite
        * isReflexive
        * notification

TODO: add support for topologies

"""

import csv
import os
import sys

import arcpy


class Toolbox(object):
    def __init__(self):
        self.label = "Describe_Database_Tool"
        self.alias = "Toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [DescribeDatabase]


class DescribeDatabase(object):
    def __init__(self):
        self.label = "Describe_Database"
        self.description = ""
        self.canRunInBackground = True

    def getParameterInfo(self):

        param0=arcpy.Parameter(
            displayName='Input Geodatabase',
            name= 'Input_Geodatabase',
            datatype= 'DEWorkspace',
            parameterType= 'required',
            direction='Input')

        param1=arcpy.Parameter(
            displayName='Output Folder Location',
            name= 'Output_Folder_Location',
            datatype= 'DEFolder',
            parameterType= 'required',
            direction='Input')
                
        params = [param0, param1]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, params):
        return

    def updateMessages(self, params):
        return

    def execute(self, params, messages):

        starting_workspace = arcpy.env.workspace
        
        gdb = params[0].valueAsText
        output_folder = params[1].valueAsText
        arcpy.AddMessage( "gdb = {}".format(gdb) )
        arcpy.AddMessage( "output {}".format(output_folder) )


        def get_tables_from_GDB():
            fcs, tbls = [], []
            for fds in arcpy.ListDatasets(feature_type='feature') + ['']:
                for fc in arcpy.ListFeatureClasses(feature_dataset=fds):
                    fcs.append(os.path.join(arcpy.env.workspace, fds, fc))
            tbl_list = arcpy.ListTables()
            if tbl_list:
                for tbl in tbl_list:
                    tbls.append(os.path.join(arcpy.env.workspace, tbl))                
                        
            return fcs, tbls


        def describe_table(table, dest_csv):
            fields = []
            for field in arcpy.ListFields(table):
                try:
                    unique = len(set([row for row in arcpy.da.SearchCursor(table, field.name)]))
                except:
                    unique = 'Unknown'
                field_desc = (
                    field.name,
                    field.aliasName, 
                    field.type,
                    field.length,
                    field.precision,
                    field.scale,
                    field.defaultValue,
                    field.domain,
                    field.editable,
                    field.isNullable,
                    field.required,
                    unique,
                    )
                fields.append(field_desc)
                
            with open(dest_csv, 'wb') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(
                    ['NAME', 'ALIAS', 'TYPE', 'LENGTH', 'PRECISION', 'SCALE',
                     'DEFAULT', 'DOMAIN', 'EDITABLE', 'ISNULLABLE', 'REQUIRED',
                     'UNIQUE'])
            
                for field in fields:
                        csvwriter.writerow(field)


        def describe_Relationships(gdb, output_folder):  
            rc_list = [c.name for c in arcpy.Describe(gdb).children
                        if c.datatype == "RelationshipClass"]
                        
            desc_list = []
            
            for rc in rc_list:  
                 rc_path = os.path.join(gdb, rc)
                 des_rc = arcpy.Describe(rc_path)  
                 rel_class_details = (
                     des_rc.originClassNames,
                     des_rc.originClassKeys,
                     des_rc.destinationClassNames,
                     des_rc.destinationClassKeys,
                     des_rc.forwardPathLabel,
                     des_rc.backwardPathLabel,
                     des_rc.cardinality,
                     des_rc.classKey,
                     des_rc.keyType,
                     des_rc.isAttributed,
                     des_rc.isComposite,
                     des_rc.isReflexive,
                     des_rc.notification)
                 desc_list.append(rel_class_details)

            if desc_list:
                with open(os.path.join(output_folder, 'RELATIONSHIP_CLASSES.csv'), 'wb') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(
                        ['ORIGIN_CLASS_NAME', 'ORIGIN_CLASS_KEY',
                         'DESTINATION_CLASS_NAME', 'DESTINATION_CLASS_KEY', 
                         'FORWARD_PATH_LABEL', 'BACKWARD_PATH_LABEL',
                         'CARDINALITY', 'CLASS_KEY', 'KEY_TYPE',
                         'IS_ATTRIBUTED', 'IS_COMPOSITE', 'IS_REFLEXIVE',
                         'NOTIFICATION'])

                    for rel_class in desc_list:
                        csvwriter.writerow(rel_class)
                        
        # Set the workspace to gdb
        arcpy.env.workspace = gdb
        
        # List all the feature classes in gdb
        fcs, tbls = get_tables_from_GDB()

        # Create a list of jobs (feature_class, output_table)    
        fc_jobs = [(fc, os.path.join(output_folder,
                    'tbl_{}.csv'.format(os.path.basename(fc))))
                    for fc in fcs]
        tbl_jobs = [(tbl, os.path.join(output_folder,
                     'tbl_{}.csv'.format(os.path.basename(tbl))))
                     for tbl in tbls]

        jobs = fc_jobs + tbl_jobs
        
        for job in jobs:
            describe_table(job[0], job[1])

        
        # Get the domains
        desc = arcpy.Describe(gdb)
        domains = desc.domains

        for domain in domains:
            table = os.path.join(output_folder,
                             '{}.csv'.format(domain.replace(' ', '_')))
        
            arcpy.DomainToTable_management(gdb, domain, table,
                                       'field', 'description', '#')

        # get the relationship classes
        describe_Relationships(gdb, output_folder)

        arcpy.env.workspace = starting_workspace
        
        return
