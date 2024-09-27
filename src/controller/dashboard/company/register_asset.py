from flask_login import current_user
from flask import jsonify

from src.model.database.company.register_patrimony.asset.create import db_create_asset

def asset_registration(asset_data, company_id):
    
    event = asset_data.get('event')
    classe = asset_data.get('classe')
    name = asset_data.get('name')
    location = asset_data.get('localization')
    acquisition_date = asset_data.get('acquisitionDate')
    acquisition_value = asset_data.get('acquisitionValue')
    status = asset_data.get('status')
    description = asset_data.get('description')

    db_create_asset(company_id, current_user.id, name, event, classe, acquisition_value, location, acquisition_date, description, status);

    return jsonify('Asset registrado com sucesso!'), 200