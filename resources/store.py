from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import uuid
from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import db
from schemas import StoreSchema
from models import StoreModel
blp = Blueprint("stores",__name__,description = "API for managing stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        # highlight-start
        store = StoreModel.query.get_or_404(store_id)
        return store
        # highlight-end

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        # highlight-start
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}, 200
        # highlight-end


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        # highlight-start
        return StoreModel.query.all()
        # highlight-end

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store