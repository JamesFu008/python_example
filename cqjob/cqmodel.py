#! /usr/bin/env python3.4

from peewee import *
import datetime

localdb = SqliteDatabase('database.db')

class BaseModel(Model):
    class Meta:
        database = localdb

class UpdateTimeModel(BaseModel):
    """ record the time the db is updated as the foreign key for the tables """
    updatetime = DateTimeField(default = datetime.datetime.now)
    update_ok = BooleanField(default = False)

class CRinfoModel(BaseModel):
    """ sheet for the active queue, CR is removed only when state is closed """    
    crid = CharField(unique = True)
    title = CharField()
    createtime = ForeignKeyField(UpdateTimeModel, related_name = 'active_CR')
    is_updated = BooleanField(default = True)
    # need key? in future
    assignee = CharField()
    # need key? in future
    department = CharField()
    project = CharField()
    bug_class = CharField()
    cr_source = CharField()
    state = CharField()
    resolvedtime = DateTimeField()
    resolution = CharField()
    # if CR is reassigned or resolved, it is out active until it is removed by closing it
    is_out_active = BooleanField(default = False)


class TransferCRModel(BaseModel):
    """ sheet for the transfer out record """
    crid = CharField(unique = True)
    transfertime = ForeignKeyField(UpdateTimeModel, related_name = 'transfer_CR')
    owner = CharField()
    new_depart = CharField()
    process_time = DateTimeField()
    department = CharField()

class ResolvedCRModel(BaseModel):
    """ sheet for the resolved CR record """
    crid = CharField(unique = True)
    resolvedtime = ForeignKeyField(UpdateTimeModel, related_name = 'resolved_CR')
    owner = CharField()
    resolution = CharField()
    process_time = DateTimeField()
    department = CharField()

class BasePointModel(BaseModel):
    number = IntegerField()
    department = CharField()

class LoadingPointModel(BasePointModel):
    """ record the time and the loading """
    querytime = ForeignKeyField(UpdateTimeModel, related_name = 'loadingpoints')

class ResolvedPointModel(BasePointModel):
    """ record the time and the resolve """
    querytime = ForeignKeyField(UpdateTimeModel, related_name = 'resolvedpoints')

class TransferPointModel(BasePointModel):
    """ record the time and the trnasfer """
    querytime = ForeignKeyField(UpdateTimeModel, related_name = 'transferpoints')

class BaseWeeklyModel(BaseModel):
    number = IntegerField(default = 0)
    # like 1501
    weeknumber = IntegerField()
    department = CharField()

class LoadingWeeklyModel(BaseWeeklyModel):
    """ record the week summary for the loading """
    pass

class ResolvedWeeklyModel(BaseWeeklyModel):
    """ record the week summary for the resolved CRs """
    pass

class TransferWeeklyModel(BaseWeeklyModel):
    """ record the week summary for the transfer """
    pass

class ProjectWeeklyModel(BaseModel):
    """ record the project summary each week """
    projectname = CharField()
    count = IntegerField(default = 0)
    # like 1501
    weeknumber = IntegerField()

__alltables = [UpdateTimeModel, CRinfoModel, TransferCRModel, 
               ResolvedCRModel, LoadingPointModel, ResolvedPointModel, TransferPointModel,
               LoadingWeeklyModel, ResolvedWeeklyModel, TransferWeeklyModel, ProjectWeeklyModel]


def table_init():
    """ called only once when create tables """
    localdb.connect()
    localdb.create_tables(__alltables)

class CQ_database:
    """ make all function in to the CQ_database """
    
    def __init__(self):
        pass

    def gettimeid(self):
        """ create the time handle and return the id """
        mymodel = UpdateTimeModel.create()
        self.timeid = mymodel.id
        return self.timeid


def modelaccess():
    """ sample code for the access """
    cqd = CQ_database()
    
    # Make time flag and get id
    timeid = cqd.gettimeid()
    print(timeid)
    # CQ login
    # Get Active Queue
    
    # write the CR database
    # make up the insert dictionary







def jtest():
    """ test function for the cqmodel test """
    #table_init()
    modelaccess()




if __name__ == "__main__":
    jtest()


