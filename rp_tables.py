# rp_tables.py
#
# Contains classes for table entries on the Real Property page. All of these classes will
# have relationships with real_property.RealProperty.

# These (will) include:
# * ValuationHistory
# * PropertyAccountStatus (low priority)
# * DeedTransaction
# * NoticeOfValue (low priority)
# * BuildingPermitHistory
# (Building was moved to buildings.py, as we are going to get the data from the building page)

from sqlalchemy import Column, Integer, Float, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from base import Base

from datetime import datetime
import requests
import get_tables
import time
import urllib3

# ValuationHistory
#
# Represents one line of the valuation history table (ie, for one year)
class ValuationHistory(Base):
    __tablename__ = "valuationhistory"

    id = Column(Integer, primary_key=True)
    local_property_id = Column(Integer, ForeignKey('realproperty.id')) # Not to be confused with "propertyid" (assigned by assessor site)
    property = relationship("RealProperty", back_populates="valuations")

    year = Column(Integer)
    market_value = Column(Integer)
    taxable_market_value = Column(Integer)
    gross_assessed = Column(Integer)
    exemption = Column(Integer)
    net_assessed = Column(Integer)
    millage = Column(Float)
    tax = Column(Float)
    tax_savings = Column(Float)

    # extract()
    #
    # Obtains data from the valuation table for a property, and returns it as a list.
    #
    # Note that this is a static method, and returns a list of ValuationHistory
    # objects.
    @staticmethod
    def extract(propertyid):
        try:
            valuation_dicts = get_tables.get_valuation_list(propertyid)
        # Occasionally the connection will fail. If so, wait a few and call the function again
        except (ConnectionError,TimeoutError,urllib3.exceptions.NewConnectionError,
                urllib3.exceptions.MaxRetryError, requests.ConnectionError) as e:
            print("Exception caught: "+str(e))
            time.sleep(10)
            return ValuationHistory.extract(propertyid)

        valuation_list = []
        for d in valuation_dicts:
            v = ValuationHistory()
            v.year = d['year']
            v.market_value = d['market_value']
            v.taxable_market_value = d['taxable_market_value']
            v.gross_assessed = d['gross_assessed']
            v.exemption = d['exemption']
            v.net_assessed = d['net_assessed']
            v.millage = d['millage']
            v.tax = d['tax']
            v.tax_savings = d['tax_savings']
            valuation_list.append(v)

        return valuation_list

class DeedTransaction(Base):
    __tablename__ = "deedtransactions"

    id = Column(Integer, primary_key=True)
    local_property_id = Column(Integer, ForeignKey('realproperty.id')) # Not to be confused with "propertyid" (assigned by assessor site)
    property = relationship("RealProperty", back_populates="deedtransactions")

    date = Column(Date)
    type = Column(String)
    book = Column(Integer) # not sure, may need to be changed to string later?
    page = Column(Integer) # not sure, may need to be changed to string later?
    price = Column(Integer)
    grantor = Column(String)
    grantee = Column(String)

    # extract()
    #
    # Obtains data from the transaction table for a property, and returns it as a list.
    #
    # Note that this is a static method, and returns a list of DeedTransaction
    # objects.
    @staticmethod
    def extract(propertyid):
        try:
            transaction_dicts = get_tables.get_transaction_list(propertyid)
        # Occasionally the connection will fail. If so, wait a few and call the function again
        except (ConnectionError,TimeoutError,urllib3.exceptions.NewConnectionError,
                urllib3.exceptions.MaxRetryError, requests.ConnectionError) as e:
            print("Exception caught: "+str(e))
            time.sleep(10)
            return DeedTransaction.extract(propertyid)

        transaction_list = []
        for d in transaction_dicts:
            t = DeedTransaction()
            t.date = datetime.strptime(d['date'], "%m/%d/%Y")
            t.type = d['type']
            t.book = d['book']
            t.page = d['page']
            t.price = d['price']
            t.grantor = d['grantor']
            t.grantee = d['grantee']

            transaction_list.append(t)

        return transaction_list




class BuildingPermit(Base):
    __tablename__ = "buildingpermits"

    id = Column(Integer, primary_key=True)
    local_property_id = Column(Integer, ForeignKey('realproperty.id')) # Not to be confused with "propertyid" (assigned by assessor site)
    property = relationship("RealProperty", back_populates="buildingpermits")

    date = Column(Date)
    permit_number = Column(String)
    provided_by = Column(String)
    building_number = Column(Integer)
    description = Column(String)
    estimated_cost = Column(Integer)
    status = Column(String)

    @staticmethod
    def extract(propertyid):
        try:
            permit_dicts = get_tables.get_permit_list(propertyid)
        # Occasionally the connection will fail. If so, wait a few and call the function again
        except (ConnectionError,TimeoutError,urllib3.exceptions.NewConnectionError,
                urllib3.exceptions.MaxRetryError, requests.ConnectionError) as e:
            print("Exception caught: "+str(e))
            time.sleep(10)
            return BuildingPermit.extract(propertyid)

        permit_list = []
        for d in permit_dicts:
            p = BuildingPermit()
            p.date = datetime.strptime(d['date'], "%m/%d/%Y")
            p.permit_number = d['permit_number']
            p.provided_by = d['provided_by']
            p.building_number = d['building_number']
            p.description = d['description']
            p.estimated_cost = d['estimated_cost']
            p.status = d['status']

            permit_list.append(p)

        return permit_list