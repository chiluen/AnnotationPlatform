from flask import Flask
from flask_cors import CORS
from api.Mainpage import mainpageApi
from api.DB import dbApi
from api.Annotation import annotationApi
from api.Review import reviewApi
from api.Signin import signinApi
from api.Register import registerApi
from api.Upload import uploadApi

app = Flask(__name__)
CORS(app)

app.config.from_mapping(
    GCLOUD_PROJECT_ID='final-annotation-351318',
    BIGTABLE_INSTANCE_ID='final-annotation',
    BIGTABLE_AUTH_ID='auth',
    BIGTABLE_ANNOTATION_ID='annotation',
)

#-----Register different API-----#
app.register_blueprint(mainpageApi, url_prefix='/mainpage')
app.register_blueprint(dbApi, url_prefix='/db')
app.register_blueprint(annotationApi, url_prefix='/annotation')
app.register_blueprint(reviewApi, url_prefix='/review')
app.register_blueprint(signinApi, url_prefix='/signin')
app.register_blueprint(registerApi, url_prefix='/register')
app.register_blueprint(uploadApi, url_prefix='/upload')

if __name__ == "__main__":
    print("Backend start")
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)
