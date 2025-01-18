class Config:
    SECRET_KEY = "Akshant"
    MONGO_URI = "mongodb+srv://doc_verify:doc1234@cluster0.ojspt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    DB_NAME = "KYC"
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = False  # Set to True for production
    JWT_ACCESS_COOKIE_NAME = "access_token"  # Use your custom cookie name
    JWT_COOKIE_CSRF_PROTECT = False 
