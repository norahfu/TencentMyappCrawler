from MongoWrapper import MongoDBWrapper

class Utils:
    @staticmethod
    def configure_mongodb(caller_class, **kwargs):
        """
        Configures the MongoDB connection wrapper
        """

        mongo_uri = MongoDBWrapper.build_mongo_uri(**kwargs)
        mongo_wrapper = MongoDBWrapper()
        caller_class._mongo_wrapper = mongo_wrapper
        return mongo_wrapper.connect(mongo_uri, kwargs['database'],
                                     kwargs['seed_collection'])
