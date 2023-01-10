from .database import Base
from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship, backref
from datetime import datetime
import enum

class ProcessingStatusType(enum.Enum):
    waiting = 1
    processing = 2
    done = 3
    error = 4

class WeatherDocument(Base):
    __tablename__ = 'weather_document'

    id = Column(Integer, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    status = Column(
        Enum(ProcessingStatusType),
        default=ProcessingStatusType.waiting,
        nullable=False,
        index=True
    )
    error_message = Column(Text, nullable=True)

    def __repr__(self):
        return 'WeatherDocument %r>' % self.id


class WeatherResult(Base):
    __tablename__ = 'weather_result'

    id = Column(Integer, primary_key=True)
    document_id = Column(
        Integer,
        ForeignKey('weather_document.id', ondelete='CASCADE'),
        index=True,
        nullable=False
    )
    document = relationship(
        'WeatherDocument',
        backref=backref('weather_results', passive_deletes=True, lazy=False)
    )
    cityId = Column(Integer, nullable=False)
    tempCelsius = Column(Float, nullable=False)
    humidity = Column(Integer, nullable=False)

class CityIds(Base):
    __tablename__ = 'cityIds'

    id = Column(Integer, primary_key=True)
    cityId = Column(Integer, nullable=False)