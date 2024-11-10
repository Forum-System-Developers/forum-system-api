import random
from uuid import uuid4
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from forum_system_api.persistence.models.admin import Admin
from forum_system_api.persistence.models.category import Category
from forum_system_api.persistence.models.conversation import Conversation
from forum_system_api.persistence.models.message import Message
from forum_system_api.persistence.models.reply import Reply
from forum_system_api.persistence.models.reply_reaction import ReplyReaction
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.user import User
from forum_system_api.persistence.models.user_category_permission import UserCategoryPermission
from forum_system_api.persistence.models.access_level import AccessLevel


def random_date_within_last_month() -> datetime:
    now = datetime.now()
    one_month_ago = now - timedelta(days=30)
    return one_month_ago + (now - one_month_ago) * random.random()


def ensure_valid_created_at(target_date: datetime) -> datetime:
    while (valid_datetime := random_date_within_last_month()) <= target_date:
        pass

    return valid_datetime


users = [
    {
        "id": uuid4(), 
        "username": "Hris", 
        "password_hash": "$2b$12$nGEjd00kxV2jpMER2BTin.WmULdDMFRMd1dpsKE0zoRYLNimVkPpG", 
        "first_name": "Hris", 
        "last_name": "Hris", 
        "email": "hris@example.com",
        "created_at": datetime.now() - timedelta(days=31)
    },
    {
        "id": uuid4(), 
        "username": "Toni", 
        "password_hash": "$2b$12$boYBBeDHIffOkm3GpRzJJuwizXGeRDfmnvlzIyigXws5sj.Pq4E9i", 
        "first_name": "Toni", 
        "last_name": "Toni", 
        "email": "toni@example.com", 
        "created_at": datetime.now() - timedelta(days=31)
    },
    {
        "id": uuid4(), 
        "username": "Miki", 
        "password_hash": "$2b$12$ozOC9v1JlmVp6lFiAvUtM.XOzS4hsY3/duVTkjmtoCOdy.ksYJMk6", 
        "first_name": "Miki", 
        "last_name": "Miki", 
        "email": "miki@example.com", 
        "created_at": datetime.now() - timedelta(days=31)
    },
    {
        "id": uuid4(), 
        "username": "john_doe", 
        "password_hash": "$2b$12$I7HlE/KMyd1xuz6iNG/ktO4S6A0hq5PvEl4BEpGFmny3XRt.rJuqe", 
        "first_name": "John", 
        "last_name": "Doe", 
        "email": "john_doe@example.com", 
        "created_at": datetime.now() - timedelta(days=31)
    },
    {
        "id": uuid4(), 
        "username": "Admin", 
        "password_hash": "$2b$12$ZPsQYktTn83HyQD7xcNS4OSGPQvymqEFq3E7WpRF3A/p3z7tS4f0S",
        "first_name": "Admin",
        "last_name": "Admin",
        "email": "admin@example.com", 
        "created_at": datetime.now() - timedelta(days=31)
    }
]


admins = [
    {
        "id": uuid4(),
        "user_id": users[4]['id'],
        "created_at": datetime.now()
    }
]


categories = [
    {
        "id": uuid4(), 
        "name": "Programming", 
        "is_private": False, 
        "is_locked": False, 
        "created_at": random_date_within_last_month()
    },
    {
        "id": uuid4(), 
        "name": "Data Science", 
        "is_private": False, 
        "is_locked": False, 
        "created_at": random_date_within_last_month()
    },
    {
        "id": uuid4(), 
        "name": "Artificial Intelligence", 
        "is_private": False, 
        "is_locked": False, 
        "created_at": random_date_within_last_month()
    },
    {
        "id": uuid4(), 
        "name": "Cybersecurity", 
        "is_private": False, 
        "is_locked": False, 
        "created_at": random_date_within_last_month()
    },
    {
        "id": uuid4(), 
        "name": "Software Engineering", 
        "is_private": False, 
        "is_locked": False, 
        "created_at": random_date_within_last_month()
    },
    {
        "id": uuid4(), 
        "name": "Computer Networks", 
        "is_private": False, 
        "is_locked": False, 
        "created_at": random_date_within_last_month()
    },
    {
        "id": uuid4(), 
        "name": "Machine Learning", 
        "is_private": False, 
        "is_locked": False, 
        "created_at": random_date_within_last_month()
    },
    {
        "id": uuid4(), 
        "name": "Cloud Computing", 
        "is_private": False, 
        "is_locked": True, 
        "created_at": random_date_within_last_month()
    },
    {
        "id": uuid4(), 
        "name": "Blockchain", 
        "is_private": True, 
        "is_locked": False, 
        "created_at": random_date_within_last_month()
    },
    {
        "id": uuid4(), 
        "name": "Quantum Computing", 
        "is_private": True, 
        "is_locked": True, 
        "created_at": random_date_within_last_month()
    },
]


programming_topics = [
    {
        "id": uuid4(),
        "title": "Best Practices in Python", 
        "content": "Discussing the best practices for writing clean and efficient Python code.", 
        "author_id": users[0]['id'], 
        "category_id": categories[0]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[0]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Getting Started with C++", 
        "content": "How to start with C++ as a beginner.", 
        "author_id": users[1]['id'], 
        "category_id": categories[0]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[0]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "JavaScript for Web Development", 
        "content": "Exploring how JavaScript enhances web development.", 
        "author_id": users[2]['id'], 
        "category_id": categories[0]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[0]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Rust: The Modern Systems Language", 
        "content": "Why Rust is becoming popular for system-level programming.", 
        "author_id": users[3]['id'], 
        "category_id": categories[0]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[0]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Understanding Object-Oriented Programming", 
        "content": "A comprehensive discussion on OOP principles.", 
        "author_id": users[0]['id'], 
        "category_id": categories[0]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[0]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Functional Programming Concepts", 
        "content": "What makes functional programming unique.", 
        "author_id": users[2]['id'], 
        "category_id": categories[0]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[0]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Asynchronous Programming in Python", 
        "content": "Exploring async and await in Python for concurrency.", 
        "author_id": users[3]['id'], 
        "category_id": categories[0]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[0]['created_at'])
    },
]


data_science_topics = [
    {
        "id": uuid4(),
        "title": "Introduction to Data Science", 
        "content": "An overview of the field of data science and its applications.", 
        "author_id": users[1]['id'], 
        "category_id": categories[1]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[1]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Machine Learning Fundamentals", 
        "content": "Understanding the basics of machine learning algorithms.", 
        "author_id": users[2]['id'], 
        "category_id": categories[1]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[1]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Data Visualization Techniques", 
        "content": "Exploring different ways to visualize data effectively.", 
        "author_id": users[3]['id'], 
        "category_id": categories[1]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[1]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Big Data Analytics", 
        "content": "How to analyze and derive insights from large datasets.", 
        "author_id": users[0]['id'], 
        "category_id": categories[1]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[1]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Deep Learning Applications", 
        "content": "Real-world applications of deep learning models.", 
        "author_id": users[1]['id'], 
        "category_id": categories[1]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[1]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Natural Language Processing", 
        "content": "Understanding how machines process and generate human language.", 
        "author_id": users[2]['id'], 
        "category_id": categories[1]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[1]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Data Science Career Paths", 
        "content": "Exploring different career opportunities in the field of data science.", 
        "author_id": users[3]['id'], 
        "category_id": categories[1]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[1]['created_at'])
    },
]


ai_topics = [
    {
        "id": uuid4(),
        "title": "Introduction to AI", 
        "content": "An overview of artificial intelligence and its subfields.", 
        "author_id": users[2]['id'], 
        "category_id": categories[2]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[2]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Neural Networks Explained", 
        "content": "Understanding the architecture and training of neural networks.", 
        "author_id": users[3]['id'], 
        "category_id": categories[2]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[2]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Computer Vision Applications", 
        "content": "Real-world applications of computer vision technology.", 
        "author_id": users[0]['id'], 
        "category_id": categories[2]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[2]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Reinforcement Learning Basics", 
        "content": "An introduction to reinforcement learning algorithms.", 
        "author_id": users[1]['id'], 
        "category_id": categories[2]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[2]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "AI Ethics and Bias", 
        "content": "Discussing ethical considerations in artificial intelligence development.", 
        "author_id": users[2]['id'], 
        "category_id": categories[2]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[2]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "AI in Healthcare", 
        "content": "Applications of AI in the healthcare industry.", 
        "author_id": users[3]['id'], 
        "category_id": categories[2]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[2]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "AI Research Trends", 
        "content": "Current trends and breakthroughs in artificial intelligence research.", 
        "author_id": users[0]['id'], 
        "category_id": categories[2]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[2]['created_at'])
    },
]


cybersecurity_topics = [
    {
        "id": uuid4(),
        "title": "Cybersecurity Fundamentals", 
        "content": "An introduction to the basics of cybersecurity.", 
        "author_id": users[3]['id'], 
        "category_id": categories[3]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[3]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Network Security Best Practices", 
        "content": "How to secure networks from cyber threats.", 
        "author_id": users[0]['id'], 
        "category_id": categories[3]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[3]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Web Application Security", 
        "content": "Protecting web applications from common security vulnerabilities.", 
        "author_id": users[1]['id'], 
        "category_id": categories[3]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[3]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Incident Response Strategies", 
        "content": "Preparing for and responding to cybersecurity incidents.", 
        "author_id": users[2]['id'], 
        "category_id": categories[3]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[3]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Cryptography Explained", 
        "content": "Understanding cryptographic algorithms and protocols.", 
        "author_id": users[3]['id'], 
        "category_id": categories[3]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[3]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Security Compliance Standards", 
        "content": "Complying with cybersecurity regulations and standards.", 
        "author_id": users[0]['id'], 
        "category_id": categories[3]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[3]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Cybersecurity Career Paths", 
        "content": "Exploring different career opportunities in the field of cybersecurity.", 
        "author_id": users[1]['id'], 
        "category_id": categories[3]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[3]['created_at'])
    },
]


software_engineering_topics = [
    {
        "id": uuid4(),
        "title": "Software Development Life Cycle", 
        "content": "Understanding the stages of software development.", 
        "author_id": users[2]['id'], 
        "category_id": categories[4]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[4]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Agile Methodologies Explained", 
        "content": "An overview of agile software development practices.", 
        "author_id": users[3]['id'], 
        "category_id": categories[4]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[4]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "DevOps Principles and Practices", 
        "content": "How DevOps improves collaboration between development and operations teams.", 
        "author_id": users[0]['id'], 
        "category_id": categories[4]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[4]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Software Testing Strategies", 
        "content": "Different approaches to testing software for quality assurance.", 
        "author_id": users[1]['id'], 
        "category_id": categories[4]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[4]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Code Refactoring Techniques", 
        "content": "Improving code quality through refactoring practices.", 
        "author_id": users[2]['id'], 
        "category_id": categories[4]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[4]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Continuous Integration and Deployment", 
        "content": "Automating the build and deployment process for software projects.", 
        "author_id": users[3]['id'], 
        "category_id": categories[4]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[4]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Software Architecture Patterns", 
        "content": "Common architectural patterns used in software design.", 
        "author_id": users[0]['id'], 
        "category_id": categories[4]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[4]['created_at'])
    },
]


computer_networks_topics = [
    {
        "id": uuid4(),
        "title": "Introduction to Networking", 
        "content": "An overview of computer networking concepts and protocols.", 
        "author_id": users[1]['id'], 
        "category_id": categories[5]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[5]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "TCP/IP Protocol Suite", 
        "content": "Understanding the TCP/IP protocol stack and its components.", 
        "author_id": users[2]['id'], 
        "category_id": categories[5]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[5]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Network Security Fundamentals", 
        "content": "Basic principles of securing computer networks.", 
        "author_id": users[3]['id'], 
        "category_id": categories[5]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[5]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Wireless Networking Technologies", 
        "content": "Exploring wireless communication standards and technologies.", 
        "author_id": users[0]['id'], 
        "category_id": categories[5]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[5]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Internet of Things (IoT)", 
        "content": "How IoT devices communicate over networks.", 
        "author_id": users[1]['id'], 
        "category_id": categories[5]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[5]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Network Troubleshooting Tips", 
        "content": "Common techniques for diagnosing and resolving network issues.", 
        "author_id": users[2]['id'], 
        "category_id": categories[5]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[5]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Network Design and Implementation", 
        "content": "Best practices for designing and deploying computer networks.", 
        "author_id": users[3]['id'], 
        "category_id": categories[5]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[5]['created_at'])
    },
]


ml_topics = [
    {
        "id": uuid4(),
        "title": "Supervised Learning Algorithms", 
        "content": "Understanding the principles and applications of supervised learning.", 
        "author_id": users[3]['id'], 
        "category_id": categories[6]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[6]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Unsupervised Learning Techniques", 
        "content": "Exploring clustering and dimensionality reduction algorithms.", 
        "author_id": users[0]['id'], 
        "category_id": categories[6]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[6]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Deep Learning Frameworks", 
        "content": "Popular libraries and tools for deep learning development.", 
        "author_id": users[1]['id'], 
        "category_id": categories[6]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[6]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Recommender Systems", 
        "content": "How recommendation engines work and their applications.", 
        "author_id": users[2]['id'], 
        "category_id": categories[6]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[6]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Natural Language Processing Models", 
        "content": "State-of-the-art models for processing and generating human language.", 
        "author_id": users[3]['id'], 
        "category_id": categories[6]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[6]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Time Series Forecasting", 
        "content": "Predictive modeling techniques for time series data.", 
        "author_id": users[0]['id'], 
        "category_id": categories[6]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[6]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Machine Learning Research Trends", 
        "content": "Current trends and breakthroughs in machine learning research.", 
        "author_id": users[1]['id'], 
        "category_id": categories[6]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[6]['created_at'])
    },
]


cloud_computing_topics = [
    {
        "id": uuid4(),
        "title": "Introduction to Cloud Computing", 
        "content": "An overview of cloud computing services and deployment models.", 
        "author_id": users[0]['id'], 
        "category_id": categories[7]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[7]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Cloud Infrastructure as a Service (IaaS)", 
        "content": "Understanding IaaS providers and their offerings.", 
        "author_id": users[1]['id'], 
        "category_id": categories[7]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[7]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Platform as a Service (PaaS) Solutions", 
        "content": "Exploring PaaS platforms for application development and deployment.", 
        "author_id": users[2]['id'], 
        "category_id": categories[7]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[7]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Software as a Service (SaaS) Applications", 
        "content": "Popular SaaS applications and their benefits.", 
        "author_id": users[3]['id'], 
        "category_id": categories[7]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[7]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Cloud Security Best Practices", 
        "content": "How to secure data and applications in the cloud.", 
        "author_id": users[0]['id'], 
        "category_id": categories[7]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[7]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Cloud Migration Strategies", 
        "content": "Planning and executing a successful cloud migration project.", 
        "author_id": users[1]['id'], 
        "category_id": categories[7]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[7]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Serverless Computing Concepts", 
        "content": "An introduction to serverless computing and its benefits.", 
        "author_id": users[2]['id'], 
        "category_id": categories[7]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[7]['created_at'])
    },
]


blockchain_topics = [
    {
        "id": uuid4(),
        "title": "Blockchain Technology Explained", 
        "content": "An overview of blockchain technology and its applications.", 
        "author_id": users[2]['id'], 
        "category_id": categories[8]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[8]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Cryptocurrencies and Digital Assets", 
        "content": "Understanding the role of cryptocurrencies in the blockchain ecosystem.", 
        "author_id": users[3]['id'], 
        "category_id": categories[8]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[8]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Smart Contracts and Decentralized Apps", 
        "content": "How smart contracts enable decentralized applications on the blockchain.", 
        "author_id": users[0]['id'], 
        "category_id": categories[8]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[8]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Blockchain Security Considerations", 
        "content": "Best practices for securing blockchain networks and assets.", 
        "author_id": users[1]['id'], 
        "category_id": categories[8]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[8]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Blockchain Governance Models", 
        "content": "Different approaches to governing blockchain networks and protocols.", 
        "author_id": users[2]['id'], 
        "category_id": categories[8]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[8]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Blockchain Use Cases in Finance", 
        "content": "Applications of blockchain technology in the financial industry.", 
        "author_id": users[3]['id'], 
        "category_id": categories[8]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[8]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Blockchain Research Trends", 
        "content": "Current trends and innovations in blockchain research and development.", 
        "author_id": users[0]['id'], 
        "category_id": categories[8]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[8]['created_at'])
    },
]


quantum_computing_topics = [
    {
        "id": uuid4(),
        "title": "Quantum Computing Fundamentals", 
        "content": "An introduction to quantum computing principles and algorithms.", 
        "author_id": users[1]['id'], 
        "category_id": categories[9]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[9]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Quantum Algorithms and Applications", 
        "content": "Exploring quantum algorithms and their potential applications.", 
        "author_id": users[2]['id'], 
        "category_id": categories[9]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[9]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Quantum Cryptography and Security", 
        "content": "How quantum principles can enhance data security and privacy.", 
        "author_id": users[3]['id'], 
        "category_id": categories[9]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[9]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Quantum Machine Learning", 
        "content": "Applications of quantum computing in machine learning and optimization.", 
        "author_id": users[0]['id'], 
        "category_id": categories[9]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[9]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Quantum Computing Hardware", 
        "content": "Current developments in quantum computing hardware and technologies.", 
        "author_id": users[1]['id'], 
        "category_id": categories[9]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[9]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Quantum Computing Research Trends", 
        "content": "Emerging trends and breakthroughs in quantum computing research.", 
        "author_id": users[2]['id'], 
        "category_id": categories[9]['id'], 
        "is_locked": False, 
        "created_at": ensure_valid_created_at(categories[9]['created_at'])
    },
    {
        "id": uuid4(),
        "title": "Quantum Computing and AI",
        "content": "How quantum computing can enhance artificial intelligence capabilities.",
        "author_id": users[3]['id'],
        "category_id": categories[9]['id'],
        "is_locked": False,
        "created_at": ensure_valid_created_at(categories[9]['created_at'])
    },
]


programming_replies = [
    {
        "id": uuid4(),
        "content": "Great topic! I've been learning Python recently and these best practices are really helpful.",
        "author_id": users[1]['id'],
        "topic_id": programming_topics[0]['id'],
        "created_at": ensure_valid_created_at(programming_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I agree! Python is a versatile language and following best practices can make your code more readable and maintainable.",
        "author_id": users[2]['id'],
        "topic_id": programming_topics[0]['id'],
        "created_at": ensure_valid_created_at(programming_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Thanks for sharing these tips! I'll keep them in mind as I continue to improve my Python skills.",
        "author_id": users[3]['id'],
        "topic_id": programming_topics[0]['id'],
        "created_at": ensure_valid_created_at(programming_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been using Python for a while now, and I can definitely vouch for the benefits of following best practices.",
        "author_id": users[0]['id'],
        "topic_id": programming_topics[0]['id'],
        "created_at": ensure_valid_created_at(programming_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "These best practices are essential for writing clean and maintainable Python code. Thanks for sharing!",
        "author_id": users[1]['id'],
        "topic_id": programming_topics[0]['id'],
        "created_at": ensure_valid_created_at(programming_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I'm new to C++ and this guide has been really helpful in getting started with the language.",
        "author_id": users[2]['id'],
        "topic_id": programming_topics[1]['id'],
        "created_at": ensure_valid_created_at(programming_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "C++ can be a bit intimidating at first, but once you get the hang of it, it's a powerful language for system-level programming.",
        "author_id": users[3]['id'],
        "topic_id": programming_topics[1]['id'],
        "created_at": ensure_valid_created_at(programming_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been using C++ for a while now, and I can say that it's a great language for building high-performance applications.",
        "author_id": users[0]['id'],
        "topic_id": programming_topics[1]['id'],
        "created_at": ensure_valid_created_at(programming_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "C++ is a powerful language with a rich set of features. It's definitely worth learning if you're interested in system-level programming.",
        "author_id": users[1]['id'],
        "topic_id": programming_topics[1]['id'],
        "created_at": ensure_valid_created_at(programming_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "JavaScript is an essential tool for web development, and understanding its features can help you build interactive and dynamic websites.",
        "author_id": users[2]['id'],
        "topic_id": programming_topics[2]['id'],
        "created_at": ensure_valid_created_at(programming_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been using JavaScript for front-end development, and I can say that it's a versatile language with a lot of useful libraries and frameworks.",
        "author_id": users[3]['id'],
        "topic_id": programming_topics[2]['id'],
        "created_at": ensure_valid_created_at(programming_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "JavaScript is a key technology for building modern web applications. It's definitely worth learning if you're interested in web development.",
        "author_id": users[0]['id'],
        "topic_id": programming_topics[2]['id'],
        "created_at": ensure_valid_created_at(programming_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "JavaScript is a versatile language that can be used for both front-end and back-end development. It's a must-have skill for web developers.",
        "author_id": users[1]['id'],
        "topic_id": programming_topics[2]['id'],
        "created_at": ensure_valid_created_at(programming_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Rust is gaining popularity for its safety features and performance benefits. It's definitely worth exploring if you're interested in system-level programming.",
        "author_id": users[2]['id'],
        "topic_id": programming_topics[3]['id'],
        "created_at": ensure_valid_created_at(programming_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been using Rust for a while now, and I can say that it's a great language for building fast and reliable software.",
        "author_id": users[3]['id'],
        "topic_id": programming_topics[3]['id'],
        "created_at": ensure_valid_created_at(programming_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Rust's memory safety features make it a great choice for systems programming. It's definitely worth learning if you're interested in low-level development.",
        "author_id": users[0]['id'],
        "topic_id": programming_topics[3]['id'],
        "created_at": ensure_valid_created_at(programming_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Rust's focus on safety and performance makes it a compelling language for building high-performance applications. It's definitely worth checking out!",
        "author_id": users[1]['id'],
        "topic_id": programming_topics[3]['id'],
        "created_at": ensure_valid_created_at(programming_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Object-oriented programming is a powerful paradigm for building modular and reusable software components. It's a key concept for software developers.",
        "author_id": users[2]['id'],
        "topic_id": programming_topics[4]['id'],
        "created_at": ensure_valid_created_at(programming_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been using OOP principles in my projects, and I can say that they've helped me write more maintainable and scalable code.",
        "author_id": users[3]['id'],
        "topic_id": programming_topics[4]['id'],
        "created_at": ensure_valid_created_at(programming_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Understanding OOP concepts is essential for building complex software systems. It's definitely worth learning if you're new to programming.",
        "author_id": users[0]['id'],
        "topic_id": programming_topics[4]['id'],
        "created_at": ensure_valid_created_at(programming_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "OOP principles can help you write more maintainable and scalable code. It's a key concept for software developers of all levels.",
        "author_id": users[1]['id'],
        "topic_id": programming_topics[4]['id'],
        "created_at": ensure_valid_created_at(programming_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Functional programming is a unique paradigm that emphasizes immutability and pure functions. It's a great way to write concise and expressive code.",
        "author_id": users[2]['id'],
        "topic_id": programming_topics[5]['id'],
        "created_at": ensure_valid_created_at(programming_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been exploring functional programming concepts, and I can say that they've helped me write more elegant and maintainable code.",
        "author_id": users[3]['id'],
        "topic_id": programming_topics[5]['id'],
        "created_at": ensure_valid_created_at(programming_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Functional programming is a powerful paradigm that can help you write more concise and expressive code. It's definitely worth learning if you're interested in software development.",
        "author_id": users[0]['id'],
        "topic_id": programming_topics[5]['id'],
        "created_at": ensure_valid_created_at(programming_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Functional programming principles can help you write more maintainable and scalable code. It's a key concept for software developers of all levels.",
        "author_id": users[1]['id'],
        "topic_id": programming_topics[5]['id'],
        "created_at": ensure_valid_created_at(programming_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Asynchronous programming in Python allows you to write concurrent code that can improve performance and responsiveness. It's a powerful feature of the language.",
        "author_id": users[2]['id'],
        "topic_id": programming_topics[6]['id'],
        "created_at": ensure_valid_created_at(programming_topics[6]['created_at'])
    },
]


data_science_replies = [
    {
        "id": uuid4(),
        "content": "Great topic! I've been learning about data science and these fundamentals are really helpful.",
        "author_id": users[1]['id'],
        "topic_id": data_science_topics[0]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I agree! Data science is a fascinating field with a wide range of applications.",
        "author_id": users[2]['id'],
        "topic_id": data_science_topics[0]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Thanks for sharing these insights! I'll keep them in mind as I continue to explore data science.",
        "author_id": users[3]['id'],
        "topic_id": data_science_topics[0]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Data science is a rapidly growing field with many exciting opportunities. It's great to see more people getting interested in it.",
        "author_id": users[0]['id'],
        "topic_id": data_science_topics[0]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "These fundamentals are essential for anyone looking to start a career in data science. Thanks for sharing!",
        "author_id": users[1]['id'],
        "topic_id": data_science_topics[0]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Machine learning is a powerful tool for analyzing and making predictions from data. It's great to see more people learning about it.",
        "author_id": users[2]['id'],
        "topic_id": data_science_topics[1]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been studying machine learning algorithms, and I can say that they're a key part of data science projects.",
        "author_id": users[3]['id'],
        "topic_id": data_science_topics[1]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Machine learning algorithms can help you uncover patterns and insights from data that would be difficult to discover manually.",
        "author_id": users[0]['id'],
        "topic_id": data_science_topics[1]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Machine learning is a fascinating field that combines statistics, computer science, and domain knowledge to solve complex problems.",
        "author_id": users[1]['id'],
        "topic_id": data_science_topics[1]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Data visualization is a powerful way to communicate insights from data. It's an essential skill for data scientists and analysts.",
        "author_id": users[2]['id'],
        "topic_id": data_science_topics[2]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on data visualization projects, and I can say that they've helped me communicate complex ideas more effectively.",
        "author_id": users[3]['id'],
        "topic_id": data_science_topics[2]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Data visualization can help you uncover patterns and insights from data that would be difficult to discover manually.",
        "author_id": users[0]['id'],
        "topic_id": data_science_topics[2]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Data visualization is a key skill for data scientists and analysts. It can help you tell compelling stories with data.",
        "author_id": users[1]['id'],
        "topic_id": data_science_topics[2]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Data preprocessing is an essential step in the data science workflow. It involves cleaning, transforming, and preparing data for analysis.",
        "author_id": users[2]['id'],
        "topic_id": data_science_topics[3]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on data preprocessing tasks, and I can say that they're a key part of any data science project.",
        "author_id": users[3]['id'],
        "topic_id": data_science_topics[3]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Data preprocessing can help you clean and prepare data for analysis, making it easier to uncover insights and patterns.",
        "author_id": users[0]['id'],
        "topic_id": data_science_topics[3]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Data preprocessing is a key step in the data science workflow. It can help you ensure that your data is clean, consistent, and ready for analysis.",
        "author_id": users[1]['id'],
        "topic_id": data_science_topics[3]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Exploratory data analysis is a critical step in the data science process. It involves exploring and visualizing data to uncover patterns and insights.",
        "author_id": users[2]['id'],
        "topic_id": data_science_topics[4]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on exploratory data analysis projects, and I can say that they've helped me understand my data better.",
        "author_id": users[3]['id'],
        "topic_id": data_science_topics[4]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Exploratory data analysis can help you uncover patterns and insights from data that would be difficult to discover manually.",
        "author_id": users[0]['id'],
        "topic_id": data_science_topics[4]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Exploratory data analysis is a key step in the data science process. It can help you understand your data and identify interesting patterns and trends.",
        "author_id": users[1]['id'],
        "topic_id": data_science_topics[4]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Machine learning models are algorithms that can learn patterns and make predictions from data. They're a key tool in the data scientist's toolkit.",
        "author_id": users[2]['id'],
        "topic_id": data_science_topics[5]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on machine learning projects, and I can say that they've helped me build predictive models for a variety of applications.",
        "author_id": users[3]['id'],
        "topic_id": data_science_topics[5]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Machine learning models can help you uncover patterns and insights from data that would be difficult to discover manually.",
        "author_id": users[0]['id'],
        "topic_id": data_science_topics[5]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Machine learning models are a key tool for data scientists and analysts. They can help you build predictive models for a wide range of applications.",
        "author_id": users[1]['id'],
        "topic_id": data_science_topics[5]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Model evaluation is a critical step in the machine learning process. It involves assessing the performance of a model on unseen data.",
        "author_id": users[2]['id'],
        "topic_id": data_science_topics[6]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on model evaluation tasks, and I can say that they're a key part of building accurate and reliable machine learning models.",
        "author_id": users[3]['id'],
        "topic_id": data_science_topics[6]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Model evaluation can help you assess the performance of your machine learning models and identify areas for improvement.",
        "author_id": users[0]['id'],
        "topic_id": data_science_topics[6]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Model evaluation is a key step in the machine learning process. It can help you ensure that your models are accurate and reliable.",
        "author_id": users[1]['id'],
        "topic_id": data_science_topics[6]['id'],
        "created_at": ensure_valid_created_at(data_science_topics[6]['created_at'])
    },
]


artificial_intelligence_replies = [
    {
        "id": uuid4(),
        "content": "Great topic! I've been learning about artificial intelligence and these concepts are really helpful.",
        "author_id": users[1]['id'],
        "topic_id": ai_topics[0]['id'],
        "created_at": ensure_valid_created_at(ai_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I agree! Artificial intelligence is a fascinating field with a wide range of applications.",
        "author_id": users[2]['id'],
        "topic_id": ai_topics[0]['id'],
        "created_at": ensure_valid_created_at(ai_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Thanks for sharing these insights! I'll keep them in mind as I continue to explore artificial intelligence.",
        "author_id": users[3]['id'],
        "topic_id": ai_topics[0]['id'],
        "created_at": ensure_valid_created_at(ai_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Artificial intelligence is a rapidly growing field with many exciting opportunities. It's great to see more people getting interested in it.",
        "author_id": users[0]['id'],
        "topic_id": ai_topics[0]['id'],
        "created_at": ensure_valid_created_at(ai_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "These concepts are essential for anyone looking to start a career in artificial intelligence. Thanks for sharing!",
        "author_id": users[1]['id'],
        "topic_id": ai_topics[0]['id'],
        "created_at": ensure_valid_created_at(ai_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Machine learning is a key technology for enabling artificial intelligence applications. Understanding machine learning algorithms and techniques is essential for AI developers.",
        "author_id": users[2]['id'],
        "topic_id": ai_topics[1]['id'],
        "created_at": ensure_valid_created_at(ai_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been studying machine learning algorithms, and I can say that they're a key part of AI projects.",
        "author_id": users[3]['id'],
        "topic_id": ai_topics[1]['id'],
        "created_at": ensure_valid_created_at(ai_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Machine learning algorithms can help you build predictive models and make decisions based on data. They're a key component of AI systems.",
        "author_id": users[0]['id'],
        "topic_id": ai_topics[1]['id'],
        "created_at": ensure_valid_created_at(ai_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Machine learning is a powerful tool for building intelligent systems that can learn from data and make decisions. It's a key concept for AI developers.",
        "author_id": users[1]['id'],
        "topic_id": ai_topics[1]['id'],
        "created_at": ensure_valid_created_at(ai_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Deep learning is a subset of machine learning that focuses on neural networks and complex data representations. Understanding deep learning concepts is essential for building advanced AI systems.",
        "author_id": users[2]['id'],
        "topic_id": ai_topics[2]['id'],
        "created_at": ensure_valid_created_at(ai_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on deep learning projects, and I can say that they've helped me build advanced AI systems that can learn from complex data.",
        "author_id": users[3]['id'],
        "topic_id": ai_topics[2]['id'],
        "created_at": ensure_valid_created_at(ai_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Deep learning algorithms can help you build advanced AI systems that can learn from complex data and make decisions. They're a key technology for AI developers.",
        "author_id": users[0]['id'],
        "topic_id": ai_topics[2]['id'],
        "created_at": ensure_valid_created_at(ai_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Deep learning is a powerful technology for building intelligent systems that can learn from complex data. It's a key concept for AI developers.",
        "author_id": users[1]['id'],
        "topic_id": ai_topics[2]['id'],
        "created_at": ensure_valid_created_at(ai_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Natural language processing is a key technology for enabling AI systems to understand and generate human language. Understanding NLP concepts is essential for building language-based AI applications.",
        "author_id": users[2]['id'],
        "topic_id": ai_topics[3]['id'],
        "created_at": ensure_valid_created_at(ai_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on NLP projects, and I can say that they've helped me build language-based AI applications that can understand and generate human language.",
        "author_id": users[3]['id'],
        "topic_id": ai_topics[3]['id'],
        "created_at": ensure_valid_created_at(ai_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "NLP algorithms can help you build language-based AI applications that can understand and generate human language. They're a key technology for AI developers.",
        "author_id": users[0]['id'],
        "topic_id": ai_topics[3]['id'],
        "created_at": ensure_valid_created_at(ai_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Natural language processing is a powerful technology for building language-based AI applications. It's a key concept for AI developers.",
        "author_id": users[1]['id'],
        "topic_id": ai_topics[3]['id'],
        "created_at": ensure_valid_created_at(ai_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Computer vision is a key technology for enabling AI systems to interpret and analyze visual information. Understanding computer vision concepts is essential for building vision-based AI applications.",
        "author_id": users[2]['id'],
        "topic_id": ai_topics[4]['id'],
        "created_at": ensure_valid_created_at(ai_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on computer vision projects, and I can say that they've helped me build vision-based AI applications that can interpret and analyze visual information.",
        "author_id": users[3]['id'],
        "topic_id": ai_topics[4]['id'],
        "created_at": ensure_valid_created_at(ai_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Computer vision algorithms can help you build vision-based AI applications that can interpret and analyze visual information. They're a key technology for AI developers.",
        "author_id": users[0]['id'],
        "topic_id": ai_topics[4]['id'],
        "created_at": ensure_valid_created_at(ai_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Computer vision is a powerful technology for building vision-based AI applications. It's a key concept for AI developers.",
        "author_id": users[1]['id'],
        "topic_id": ai_topics[4]['id'],
        "created_at": ensure_valid_created_at(ai_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Reinforcement learning is a subset of machine learning that focuses on training agents to make decisions in an environment. Understanding reinforcement learning concepts is essential for building autonomous AI systems.",
        "author_id": users[2]['id'],
        "topic_id": ai_topics[5]['id'],
        "created_at": ensure_valid_created_at(ai_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on reinforcement learning projects, and I can say that they've helped me build autonomous AI systems that can make decisions in complex environments.",
        "author_id": users[3]['id'],
        "topic_id": ai_topics[5]['id'],
        "created_at": ensure_valid_created_at(ai_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Reinforcement learning algorithms can help you build autonomous AI systems that can make decisions in complex environments. They're a key technology for AI developers.",
        "author_id": users[0]['id'],
        "topic_id": ai_topics[5]['id'],
        "created_at": ensure_valid_created_at(ai_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Reinforcement learning is a powerful technology for building autonomous AI systems. It's a key concept for AI developers.",
        "author_id": users[1]['id'],
        "topic_id": ai_topics[5]['id'],
        "created_at": ensure_valid_created_at(ai_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "AI ethics is a critical aspect of developing responsible and ethical AI systems. Understanding ethical considerations and best practices is essential for AI developers and researchers.",
        "author_id": users[2]['id'],
        "topic_id": ai_topics[6]['id'],
        "created_at": ensure_valid_created_at(ai_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on AI ethics projects, and I can say that they've helped me develop responsible and ethical AI systems.",
        "author_id": users[3]['id'],
        "topic_id": ai_topics[6]['id'],
        "created_at": ensure_valid_created_at(ai_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "AI ethics is a key consideration for AI developers and researchers. It's important to build systems that are fair, transparent, and accountable.",
        "author_id": users[0]['id'],
        "topic_id": ai_topics[6]['id'],
        "created_at": ensure_valid_created_at(ai_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "AI ethics is a critical aspect of developing responsible and ethical AI systems. It's essential for building systems that are fair, transparent, and accountable.",
        "author_id": users[1]['id'],
        "topic_id": ai_topics[6]['id'],
        "created_at": ensure_valid_created_at(ai_topics[6]['created_at'])
    },
]


computer_networks_replies = [
    {
        "id": uuid4(),
        "content": "Great topic! I've been learning about networking and these concepts are really helpful.",
        "author_id": users[1]['id'],
        "topic_id": computer_networks_topics[0]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I agree! Networking is a fascinating field with a wide range of applications.",
        "author_id": users[2]['id'],
        "topic_id": computer_networks_topics[0]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Thanks for sharing these insights! I'll keep them in mind as I continue to explore computer networking.",
        "author_id": users[3]['id'],
        "topic_id": computer_networks_topics[0]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Networking is a rapidly growing field with many exciting opportunities. It's great to see more people getting interested in it.",
        "author_id": users[0]['id'],
        "topic_id": computer_networks_topics[0]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "These concepts are essential for anyone looking to start a career in computer networking. Thanks for sharing!",
        "author_id": users[1]['id'],
        "topic_id": computer_networks_topics[0]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "TCP/IP is the backbone of the internet and understanding its components is essential for network engineers and administrators.",
        "author_id": users[2]['id'],
        "topic_id": computer_networks_topics[1]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been studying TCP/IP protocols, and I can say that they're a key part of network communication.",
        "author_id": users[3]['id'],
        "topic_id": computer_networks_topics[1]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "TCP/IP protocols can help you establish reliable and secure connections between devices on a network.",
        "author_id": users[0]['id'],
        "topic_id": computer_networks_topics[1]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "TCP/IP is a fundamental protocol suite for network communication. It's a key concept for network engineers and administrators.",
        "author_id": users[1]['id'],
        "topic_id": computer_networks_topics[1]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Network security is a critical aspect of modern computing. Understanding security threats and countermeasures is essential for protecting data and systems.",
        "author_id": users[2]['id'],
        "topic_id": computer_networks_topics[2]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on network security projects, and I can say that they've helped me secure my systems and data.",
        "author_id": users[3]['id'],
        "topic_id": computer_networks_topics[2]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Network security is a key concern for organizations and individuals. It's important to stay informed about the latest threats and vulnerabilities.",
        "author_id": users[0]['id'],
        "topic_id": computer_networks_topics[2]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Network security is a critical aspect of modern computing. It's essential for protecting data and systems from cyber threats.",
        "author_id": users[1]['id'],
        "topic_id": computer_networks_topics[2]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Wireless networking is a key technology for enabling mobile and IoT devices to connect to the internet. Understanding wireless protocols and security is essential for network engineers.",
        "author_id": users[2]['id'],
        "topic_id": computer_networks_topics[3]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working with wireless networks, and I can say that they're a key part of modern computing.",
        "author_id": users[3]['id'],
        "topic_id": computer_networks_topics[3]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Wireless networking is a key technology for enabling mobile and IoT devices to connect to the internet. It's essential for network engineers and administrators.",
        "author_id": users[0]['id'],
        "topic_id": computer_networks_topics[3]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Wireless networking is a critical aspect of modern computing. It's essential for enabling mobile and IoT devices to connect to the internet.",
        "author_id": users[1]['id'],
        "topic_id": computer_networks_topics[3]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Network protocols are the rules and conventions that govern communication between devices on a network. Understanding common protocols is essential for network engineers and administrators.",
        "author_id": users[2]['id'],
        "topic_id": computer_networks_topics[4]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been studying network protocols, and I can say that they're a key part of network communication.",
        "author_id": users[3]['id'],
        "topic_id": computer_networks_topics[4]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Network protocols are essential for enabling communication between devices on a network. It's important to understand how they work and how to troubleshoot issues.",
        "author_id": users[0]['id'],
        "topic_id": computer_networks_topics[4]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Network protocols are a key concept for network engineers and administrators. They help ensure that devices can communicate effectively and securely.",
        "author_id": users[1]['id'],
        "topic_id": computer_networks_topics[4]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Network troubleshooting is a critical skill for network engineers and administrators. It involves identifying and resolving issues that can affect network performance and reliability.",
        "author_id": users[2]['id'],
        "topic_id": computer_networks_topics[5]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on network troubleshooting tasks, and I can say that they've helped me diagnose and resolve network issues more effectively.",
        "author_id": users[3]['id'],
        "topic_id": computer_networks_topics[5]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Network troubleshooting is a key skill for network engineers and administrators. It can help you identify and resolve issues that can affect network performance.",
        "author_id": users[0]['id'],
        "topic_id": computer_networks_topics[5]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Network troubleshooting is a critical aspect of modern computing. It's essential for maintaining network performance and reliability.",
        "author_id": users[1]['id'],
        "topic_id": computer_networks_topics[5]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Network monitoring is a critical aspect of modern computing. It involves tracking and analyzing network performance and security to ensure optimal operation.",
        "author_id": users[2]['id'],
        "topic_id": computer_networks_topics[6]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on network monitoring tasks, and I can say that they've helped me identify and address issues that can affect network performance.",
        "author_id": users[3]['id'],
        "topic_id": computer_networks_topics[6]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Network monitoring is a key practice for network engineers and administrators. It can help you ensure that your network is operating at peak performance.",
        "author_id": users[0]['id'],
        "topic_id": computer_networks_topics[6]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Network monitoring is a critical aspect of modern computing. It's essential for maintaining network performance and security.",
        "author_id": users[1]['id'],
        "topic_id": computer_networks_topics[6]['id'],
        "created_at": ensure_valid_created_at(computer_networks_topics[6]['created_at'])
    },
]


cybersecurity_replies = [
    {
        "id": uuid4(),
        "content": "Great topic! I've been learning about cybersecurity and these concepts are really helpful.",
        "author_id": users[1]['id'],
        "topic_id": cybersecurity_topics[0]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I agree! Cybersecurity is a critical field with a wide range of applications.",
        "author_id": users[2]['id'],
        "topic_id": cybersecurity_topics[0]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Thanks for sharing these insights! I'll keep them in mind as I continue to explore cybersecurity.",
        "author_id": users[3]['id'],
        "topic_id": cybersecurity_topics[0]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Cybersecurity is a rapidly growing field with many exciting opportunities. It's great to see more people getting interested in it.",
        "author_id": users[0]['id'],
        "topic_id": cybersecurity_topics[0]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "These concepts are essential for anyone looking to start a career in cybersecurity. Thanks for sharing!",
        "author_id": users[1]['id'],
        "topic_id": cybersecurity_topics[0]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Network security is a critical aspect of modern computing. Understanding security threats and countermeasures is essential for protecting data and systems.",
        "author_id": users[2]['id'],
        "topic_id": cybersecurity_topics[1]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on network security projects, and I can say that they've helped me secure my systems and data.",
        "author_id": users[3]['id'],
        "topic_id": cybersecurity_topics[1]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Network security is a key concern for organizations and individuals. It's important to stay informed about the latest threats and vulnerabilities.",
        "author_id": users[0]['id'],
        "topic_id": cybersecurity_topics[1]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Network security is a critical aspect of modern computing. It's essential for protecting data and systems from cyber threats.",
        "author_id": users[1]['id'],
        "topic_id": cybersecurity_topics[1]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Cryptography is a key technology for securing data and communications. Understanding cryptographic algorithms and protocols is essential for cybersecurity professionals.",
        "author_id": users[2]['id'],
        "topic_id": cybersecurity_topics[2]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been studying cryptographic algorithms, and I can say that they're a key part of securing data and communications.",
        "author_id": users[3]['id'],
        "topic_id": cybersecurity_topics[2]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Cryptography is a key technology for securing data and communications. It's essential for cybersecurity professionals.",
        "author_id": users[0]['id'],
        "topic_id": cybersecurity_topics[2]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Cryptography is a critical aspect of modern computing. It's essential for securing data and communications from unauthorized access.",
        "author_id": users[1]['id'],
        "topic_id": cybersecurity_topics[2]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Penetration testing is a key practice for identifying and addressing security vulnerabilities in systems and networks. It's a critical skill for cybersecurity professionals.",
        "author_id": users[2]['id'],
        "topic_id": cybersecurity_topics[3]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on penetration testing projects, and I can say that they've helped me identify and address security vulnerabilities more effectively.",
        "author_id": users[3]['id'],
        "topic_id": cybersecurity_topics[3]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Penetration testing is a key practice for identifying and addressing security vulnerabilities in systems and networks. It's essential for cybersecurity professionals.",
        "author_id": users[0]['id'],
        "topic_id": cybersecurity_topics[3]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Penetration testing is a critical aspect of modern computing. It's essential for identifying and addressing security vulnerabilities in systems and networks.",
        "author_id": users[1]['id'],
        "topic_id": cybersecurity_topics[3]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Incident response is a key practice for addressing security incidents and breaches. It involves detecting, analyzing, and responding to security threats in a timely manner.",
        "author_id": users[2]['id'],
        "topic_id": cybersecurity_topics[4]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on incident response tasks, and I can say that they've helped me respond to security incidents more effectively.",
        "author_id": users[3]['id'],
        "topic_id": cybersecurity_topics[4]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Incident response is a key practice for addressing security incidents and breaches. It's essential for cybersecurity professionals.",
        "author_id": users[0]['id'],
        "topic_id": cybersecurity_topics[4]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Incident response is a critical aspect of modern computing. It's essential for detecting, analyzing, and responding to security threats in a timely manner.",
        "author_id": users[1]['id'],
        "topic_id": cybersecurity_topics[4]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Security awareness training is a key practice for educating employees about security best practices and policies. It's essential for creating a security-conscious culture within an organization.",
        "author_id": users[2]['id'],
        "topic_id": cybersecurity_topics[5]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on security awareness training programs, and I can say that they've helped me educate employees about security best practices and policies.",
        "author_id": users[3]['id'],
        "topic_id": cybersecurity_topics[5]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Security awareness training is a key practice for educating employees about security best practices and policies. It's essential for creating a security-conscious culture within an organization.",
        "author_id": users[0]['id'],
        "topic_id": cybersecurity_topics[5]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Security awareness training is a critical aspect of modern computing. It's essential for educating employees about security best practices and policies.",
        "author_id": users[1]['id'],
        "topic_id": cybersecurity_topics[5]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Security compliance is a key practice for ensuring that organizations adhere to security regulations and standards. It involves implementing policies and controls to protect data and systems.",
        "author_id": users[2]['id'],
        "topic_id": cybersecurity_topics[6]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on security compliance programs, and I can say that they've helped me ensure that my organization meets security regulations and standards.",
        "author_id": users[3]['id'],
        "topic_id": cybersecurity_topics[6]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Security compliance is a key practice for ensuring that organizations adhere to security regulations and standards. It's essential for protecting data and systems.",
        "author_id": users[0]['id'],
        "topic_id": cybersecurity_topics[6]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Security compliance is a critical aspect of modern computing. It's essential for ensuring that organizations protect data and systems from security threats.",
        "author_id": users[1]['id'],
        "topic_id": cybersecurity_topics[6]['id'],
        "created_at": ensure_valid_created_at(cybersecurity_topics[6]['created_at'])
    },
]


software_engineering_replies = [
    {
        "id": uuid4(),
        "content": "Great topic! I've been learning about software engineering and these concepts are really helpful.",
        "author_id": users[1]['id'],
        "topic_id": software_engineering_topics[0]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I agree! Software engineering is a critical field with a wide range of applications.",
        "author_id": users[2]['id'],
        "topic_id": software_engineering_topics[0]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Thanks for sharing these insights! I'll keep them in mind as I continue to explore software engineering.",
        "author_id": users[3]['id'],
        "topic_id": software_engineering_topics[0]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Software engineering is a rapidly growing field with many exciting opportunities. It's great to see more people getting interested in it.",
        "author_id": users[0]['id'],
        "topic_id": software_engineering_topics[0]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "These concepts are essential for anyone looking to start a career in software engineering. Thanks for sharing!",
        "author_id": users[1]['id'],
        "topic_id": software_engineering_topics[0]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Agile software development is a key methodology for building software in an iterative and incremental manner. It's a popular approach for modern software projects.",
        "author_id": users[2]['id'],
        "topic_id": software_engineering_topics[1]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on agile software development projects, and I can say that they've helped me build software more efficiently and collaboratively.",
        "author_id": users[3]['id'],
        "topic_id": software_engineering_topics[1]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Agile software development is a key methodology for building software in an iterative and incremental manner. It's a popular approach for modern software projects.",
        "author_id": users[0]['id'],
        "topic_id": software_engineering_topics[1]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Agile software development is a critical aspect of modern software engineering. It's essential for building software that meets customer needs and adapts to changing requirements.",
        "author_id": users[1]['id'],
        "topic_id": software_engineering_topics[1]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Software testing is a critical practice for ensuring the quality and reliability of software. It involves identifying defects and verifying that software meets requirements.",
        "author_id": users[2]['id'],
        "topic_id": software_engineering_topics[2]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on software testing projects, and I can say that they've helped me identify defects and ensure the quality of software.",
        "author_id": users[3]['id'],
        "topic_id": software_engineering_topics[2]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Software testing is a key practice for ensuring the quality and reliability of software. It's essential for building software that meets customer needs and performs as expected.",
        "author_id": users[0]['id'],
        "topic_id": software_engineering_topics[2]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Software testing is a critical aspect of modern software engineering. It's essential for identifying defects and ensuring the quality of software.",
        "author_id": users[1]['id'],
        "topic_id": software_engineering_topics[2]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Software architecture is a key practice for designing and structuring software systems. It involves making high-level design decisions and defining the components and interactions of a system.",
        "author_id": users[2]['id'],
        "topic_id": software_engineering_topics[3]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on software architecture projects, and I can say that they've helped me design and structure software systems more effectively.",
        "author_id": users[3]['id'],
        "topic_id": software_engineering_topics[3]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Software architecture is a key practice for designing and structuring software systems. It's essential for building software that meets customer needs and performs as expected.",
        "author_id": users[0]['id'],
        "topic_id": software_engineering_topics[3]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Software architecture is a critical aspect of modern software engineering. It's essential for making high-level design decisions and defining the components and interactions of a system.",
        "author_id": users[1]['id'],
        "topic_id": software_engineering_topics[3]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Version control is a critical practice for managing changes to software code and collaborating with other developers. It involves tracking changes, resolving conflicts, and ensuring that code is up to date.",
        "author_id": users[2]['id'],
        "topic_id": software_engineering_topics[4]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working with version control systems, and I can say that they've helped me manage changes to software code more effectively.",
        "author_id": users[3]['id'],
        "topic_id": software_engineering_topics[4]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Version control is a key practice for managing changes to software code and collaborating with other developers. It's essential for ensuring that code is up to date and that changes are tracked and documented.",
        "author_id": users[0]['id'],
        "topic_id": software_engineering_topics[4]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Version control is a critical aspect of modern software engineering. It's essential for managing changes to software code and collaborating with other developers.",
        "author_id": users[1]['id'],
        "topic_id": software_engineering_topics[4]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Code review is a key practice for ensuring the quality and maintainability of software code. It involves reviewing code changes, providing feedback, and identifying potential issues.",
        "author_id": users[2]['id'],
        "topic_id": software_engineering_topics[5]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been participating in code reviews, and I can say that they've helped me improve the quality and maintainability of my code.",
        "author_id": users[3]['id'],
        "topic_id": software_engineering_topics[5]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Code review is a key practice for ensuring the quality and maintainability of software code. It's essential for identifying potential issues and improving code quality.",
        "author_id": users[0]['id'],
        "topic_id": software_engineering_topics[5]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Code review is a critical aspect of modern software engineering. It's essential for improving code quality and ensuring that software is maintainable and reliable.",
        "author_id": users[1]['id'],
        "topic_id": software_engineering_topics[5]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Software deployment is a key practice for releasing software to production environments. It involves preparing software for deployment, testing it in production, and monitoring its performance.",
        "author_id": users[2]['id'],
        "topic_id": software_engineering_topics[6]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on software deployment projects, and I can say that they've helped me release software more efficiently and reliably.",
        "author_id": users[3]['id'],
        "topic_id": software_engineering_topics[6]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Software deployment is a key practice for releasing software to production environments. It's essential for ensuring that software is released efficiently and reliably.",
        "author_id": users[0]['id'],
        "topic_id": software_engineering_topics[6]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Software deployment is a critical aspect of modern software engineering. It's essential for releasing software to production environments and ensuring that it performs as expected.",
        "author_id": users[1]['id'],
        "topic_id": software_engineering_topics[6]['id'],
        "created_at": ensure_valid_created_at(software_engineering_topics[6]['created_at'])
    },
]


machine_learning_replies = [
    {
        "id": uuid4(),
        "content": "Great topic! I've been learning about machine learning and these concepts are really helpful.",
        "author_id": users[1]['id'],
        "topic_id": ml_topics[0]['id'],
        "created_at": ensure_valid_created_at(ml_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I agree! Machine learning is a critical field with a wide range of applications.",
        "author_id": users[2]['id'],
        "topic_id": ml_topics[0]['id'],
        "created_at": ensure_valid_created_at(ml_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Thanks for sharing these insights! I'll keep them in mind as I continue to explore machine learning.",
        "author_id": users[3]['id'],
        "topic_id": ml_topics[0]['id'],
        "created_at": ensure_valid_created_at(ml_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Machine learning is a rapidly growing field with many exciting opportunities. It's great to see more people getting interested in it.",
        "author_id": users[0]['id'],
        "topic_id": ml_topics[0]['id'],
        "created_at": ensure_valid_created_at(ml_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "These concepts are essential for anyone looking to start a career in machine learning. Thanks for sharing!",
        "author_id": users[1]['id'],
        "topic_id": ml_topics[0]['id'],
        "created_at": ensure_valid_created_at(ml_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Supervised learning is a key machine learning technique for training models on labeled data. It's a popular approach for building predictive models.",
        "author_id": users[2]['id'],
        "topic_id": ml_topics[1]['id'],
        "created_at": ensure_valid_created_at(ml_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on supervised learning projects, and I can say that they've helped me build predictive models more effectively.",
        "author_id": users[3]['id'],
        "topic_id": ml_topics[1]['id'],
        "created_at": ensure_valid_created_at(ml_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Supervised learning is a key machine learning technique for training models on labeled data. It's a popular approach for building predictive models.",
        "author_id": users[0]['id'],
        "topic_id": ml_topics[1]['id'],
        "created_at": ensure_valid_created_at(ml_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Supervised learning is a critical aspect of modern machine learning. It's essential for building predictive models that can make accurate predictions based on labeled data.",
        "author_id": users[1]['id'],
        "topic_id": ml_topics[1]['id'],
        "created_at": ensure_valid_created_at(ml_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Unsupervised learning is a key machine learning technique for training models on unlabeled data. It's a popular approach for clustering and dimensionality reduction.",
        "author_id": users[2]['id'],
        "topic_id": ml_topics[2]['id'],
        "created_at": ensure_valid_created_at(ml_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on unsupervised learning projects, and I can say that they've helped me cluster and reduce the dimensionality of data more effectively.",
        "author_id": users[3]['id'],
        "topic_id": ml_topics[2]['id'],
        "created_at": ensure_valid_created_at(ml_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Unsupervised learning is a key machine learning technique for training models on unlabeled data. It's a popular approach for clustering and dimensionality reduction.",
        "author_id": users[0]['id'],
        "topic_id": ml_topics[2]['id'],
        "created_at": ensure_valid_created_at(ml_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Unsupervised learning is a critical aspect of modern machine learning. It's essential for clustering data and reducing its dimensionality without labeled examples.",
        "author_id": users[1]['id'],
        "topic_id": ml_topics[2]['id'],
        "created_at": ensure_valid_created_at(ml_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Reinforcement learning is a key machine learning technique for training agents to interact with an environment and learn from feedback. It's a popular approach for building autonomous systems.",
        "author_id": users[2]['id'],
        "topic_id": ml_topics[3]['id'],
        "created_at": ensure_valid_created_at(ml_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on reinforcement learning projects, and I can say that they've helped me build agents that can learn from feedback and interact with environments more effectively.",
        "author_id": users[3]['id'],
        "topic_id": ml_topics[3]['id'],
        "created_at": ensure_valid_created_at(ml_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Reinforcement learning is a key machine learning technique for training agents to interact with an environment and learn from feedback. It's a popular approach for building autonomous systems.",
        "author_id": users[0]['id'],
        "topic_id": ml_topics[3]['id'],
        "created_at": ensure_valid_created_at(ml_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Reinforcement learning is a critical aspect of modern machine learning. It's essential for building agents that can learn from feedback and interact with environments to achieve specific goals.",
        "author_id": users[1]['id'],
        "topic_id": ml_topics[3]['id'],
        "created_at": ensure_valid_created_at(ml_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Deep learning is a key machine learning technique for training neural networks on large amounts of data. It's a popular approach for building complex models for image and speech recognition.",
        "author_id": users[2]['id'],
        "topic_id": ml_topics[4]['id'],
        "created_at": ensure_valid_created_at(ml_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on deep learning projects, and I can say that they've helped me build complex models for image and speech recognition more effectively.",
        "author_id": users[3]['id'],
        "topic_id": ml_topics[4]['id'],
        "created_at": ensure_valid_created_at(ml_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Deep learning is a key machine learning technique for training neural networks on large amounts of data. It's a popular approach for building complex models for image and speech recognition.",
        "author_id": users[0]['id'],
        "topic_id": ml_topics[4]['id'],
        "created_at": ensure_valid_created_at(ml_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Deep learning is a critical aspect of modern machine learning. It's essential for building complex models that can learn from large amounts of data and make accurate predictions.",
        "author_id": users[1]['id'],
        "topic_id": ml_topics[4]['id'],
        "created_at": ensure_valid_created_at(ml_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Natural language processing is a key machine learning technique for analyzing and generating human language. It's a popular approach for building chatbots and language translation systems.",
        "author_id": users[2]['id'],
        "topic_id": ml_topics[5]['id'],
        "created_at": ensure_valid_created_at(ml_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on natural language processing projects, and I can say that they've helped me analyze and generate human language more effectively.",
        "author_id": users[3]['id'],
        "topic_id": ml_topics[5]['id'],
        "created_at": ensure_valid_created_at(ml_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Natural language processing is a key machine learning technique for analyzing and generating human language. It's a popular approach for building chatbots and language translation systems.",
        "author_id": users[0]['id'],
        "topic_id": ml_topics[5]['id'],
        "created_at": ensure_valid_created_at(ml_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Natural language processing is a critical aspect of modern machine learning. It's essential for building chatbots and language translation systems that can analyze and generate human language.",
        "author_id": users[1]['id'],
        "topic_id": ml_topics[5]['id'],
        "created_at": ensure_valid_created_at(ml_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Model evaluation is a key practice for assessing the performance of machine learning models. It involves measuring accuracy, precision, recall, and other metrics to determine how well a model performs.",
        "author_id": users[2]['id'],
        "topic_id": ml_topics[6]['id'],
        "created_at": ensure_valid_created_at(ml_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on model evaluation tasks, and I can say that they've helped me assess the performance of machine learning models more effectively.",
        "author_id": users[3]['id'],
        "topic_id": ml_topics[6]['id'],
        "created_at": ensure_valid_created_at(ml_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Model evaluation is a key practice for assessing the performance of machine learning models. It's essential for determining how well a model performs and identifying areas for improvement.",
        "author_id": users[0]['id'],
        "topic_id": ml_topics[6]['id'],
        "created_at": ensure_valid_created_at(ml_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Model evaluation is a critical aspect of modern machine learning. It's essential for measuring the accuracy, precision, recall, and other metrics of machine learning models to determine how well they perform.",
        "author_id": users[1]['id'],
        "topic_id": ml_topics[6]['id'],
        "created_at": ensure_valid_created_at(ml_topics[6]['created_at'])
    },
]


cloud_computing_replies = [
    {
        "id": uuid4(),
        "content": "Great topic! I've been learning about cloud computing and these concepts are really helpful.",
        "author_id": users[1]['id'],
        "topic_id": cloud_computing_topics[0]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I agree! Cloud computing is a critical field with a wide range of applications.",
        "author_id": users[2]['id'],
        "topic_id": cloud_computing_topics[0]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Thanks for sharing these insights! I'll keep them in mind as I continue to explore cloud computing.",
        "author_id": users[3]['id'],
        "topic_id": cloud_computing_topics[0]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Cloud computing is a rapidly growing field with many exciting opportunities. It's great to see more people getting interested in it.",
        "author_id": users[0]['id'],
        "topic_id": cloud_computing_topics[0]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "These concepts are essential for anyone looking to start a career in cloud computing. Thanks for sharing!",
        "author_id": users[1]['id'],
        "topic_id": cloud_computing_topics[0]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Infrastructure as a Service (IaaS) is a key cloud computing service model that provides virtualized computing resources over the internet. It's a popular approach for building scalable and flexible IT environments.",
        "author_id": users[2]['id'],
        "topic_id": cloud_computing_topics[1]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working with Infrastructure as a Service (IaaS) providers, and I can say that they've helped me build scalable and flexible IT environments more effectively.",
        "author_id": users[3]['id'],
        "topic_id": cloud_computing_topics[1]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Infrastructure as a Service (IaaS) is a key cloud computing service model that provides virtualized computing resources over the internet. It's a popular approach for building scalable and flexible IT environments.",
        "author_id": users[0]['id'],
        "topic_id": cloud_computing_topics[1]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Infrastructure as a Service (IaaS) is a critical aspect of modern cloud computing. It's essential for providing virtualized computing resources over the internet to build scalable and flexible IT environments.",
        "author_id": users[1]['id'],
        "topic_id": cloud_computing_topics[1]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Platform as a Service (PaaS) is a key cloud computing service model that provides a platform for developing, testing, and deploying applications over the internet. It's a popular approach for building and managing software applications.",
        "author_id": users[2]['id'],
        "topic_id": cloud_computing_topics[2]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working with Platform as a Service (PaaS) providers, and I can say that they've helped me develop, test, and deploy applications more effectively.",
        "author_id": users[3]['id'],
        "topic_id": cloud_computing_topics[2]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Platform as a Service (PaaS) is a key cloud computing service model that provides a platform for developing, testing, and deploying applications over the internet. It's a popular approach for building and managing software applications.",
        "author_id": users[0]['id'],
        "topic_id": cloud_computing_topics[2]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Platform as a Service (PaaS) is a critical aspect of modern cloud computing. It's essential for providing a platform for developing, testing, and deploying applications over the internet to build and manage software applications.",
        "author_id": users[1]['id'],
        "topic_id": cloud_computing_topics[2]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Software as a Service (SaaS) is a key cloud computing service model that provides software applications over the internet. It's a popular approach for delivering software to end users on a subscription basis.",
        "author_id": users[2]['id'],
        "topic_id": cloud_computing_topics[3]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working with Software as a Service (SaaS) providers, and I can say that they've helped me deliver software applications to end users more effectively.",
        "author_id": users[3]['id'],
        "topic_id": cloud_computing_topics[3]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Software as a Service (SaaS) is a key cloud computing service model that provides software applications over the internet. It's a popular approach for delivering software to end users on a subscription basis.",
        "author_id": users[0]['id'],
        "topic_id": cloud_computing_topics[3]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Software as a Service (SaaS) is a critical aspect of modern cloud computing. It's essential for providing software applications over the internet to deliver software to end users on a subscription basis.",
        "author_id": users[1]['id'],
        "topic_id": cloud_computing_topics[3]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Cloud storage is a key cloud computing service that provides scalable and secure storage over the internet. It's a popular approach for storing and managing data in the cloud.",
        "author_id": users[2]['id'],
        "topic_id": cloud_computing_topics[4]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working with cloud storage providers, and I can say that they've helped me store and manage data in the cloud more effectively.",
        "author_id": users[3]['id'],
        "topic_id": cloud_computing_topics[4]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Cloud storage is a key cloud computing service that provides scalable and secure storage over the internet. It's a popular approach for storing and managing data in the cloud.",
        "author_id": users[0]['id'],
        "topic_id": cloud_computing_topics[4]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Cloud storage is a critical aspect of modern cloud computing. It's essential for providing scalable and secure storage over the internet to store and manage data in the cloud.",
        "author_id": users[1]['id'],
        "topic_id": cloud_computing_topics[4]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Cloud networking is a key cloud computing service that provides scalable and secure networking over the internet. It's a popular approach for connecting cloud resources and users.",
        "author_id": users[2]['id'],
        "topic_id": cloud_computing_topics[5]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working with cloud networking providers, and I can say that they've helped me connect cloud resources and users more effectively.",
        "author_id": users[3]['id'],
        "topic_id": cloud_computing_topics[5]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Cloud networking is a key cloud computing service that provides scalable and secure networking over the internet. It's a popular approach for connecting cloud resources and users.",
        "author_id": users[0]['id'],
        "topic_id": cloud_computing_topics[5]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Cloud networking is a critical aspect of modern cloud computing. It's essential for providing scalable and secure networking over the internet to connect cloud resources and users.",
        "author_id": users[1]['id'],
        "topic_id": cloud_computing_topics[5]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Cloud security is a key practice for protecting cloud resources and data from security threats. It involves implementing security controls, monitoring for threats, and responding to incidents.",
        "author_id": users[2]['id'],
        "topic_id": cloud_computing_topics[6]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on cloud security projects, and I can say that they've helped me protect cloud resources and data from security threats more effectively.",
        "author_id": users[3]['id'],
        "topic_id": cloud_computing_topics[6]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Cloud security is a key practice for protecting cloud resources and data from security threats. It's essential for implementing security controls, monitoring for threats, and responding to incidents.",
        "author_id": users[0]['id'],
        "topic_id": cloud_computing_topics[6]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Cloud security is a critical aspect of modern cloud computing. It's essential for protecting cloud resources and data from security threats by implementing security controls, monitoring for threats, and responding to incidents.",
        "author_id": users[1]['id'],
        "topic_id": cloud_computing_topics[6]['id'],
        "created_at": ensure_valid_created_at(cloud_computing_topics[6]['created_at'])
    },
]


blockchain_replies = [
    {
        "id": uuid4(),
        "content": "Great topic! I've been learning about blockchain and these concepts are really helpful.",
        "author_id": users[1]['id'],
        "topic_id": blockchain_topics[0]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I agree! Blockchain is a critical field with a wide range of applications.",
        "author_id": users[2]['id'],
        "topic_id": blockchain_topics[0]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Thanks for sharing these insights! I'll keep them in mind as I continue to explore blockchain.",
        "author_id": users[3]['id'],
        "topic_id": blockchain_topics[0]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Blockchain is a rapidly growing field with many exciting opportunities. It's great to see more people getting interested in it.",
        "author_id": users[0]['id'],
        "topic_id": blockchain_topics[0]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "These concepts are essential for anyone looking to start a career in blockchain. Thanks for sharing!",
        "author_id": users[1]['id'],
        "topic_id": blockchain_topics[0]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Distributed ledger technology is a key blockchain concept that enables data to be stored and shared across multiple locations. It's a popular approach for building transparent and secure systems.",
        "author_id": users[2]['id'],
        "topic_id": blockchain_topics[1]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working with distributed ledger technology, and I can say that it's helped me build transparent and secure systems more effectively.",
        "author_id": users[3]['id'],
        "topic_id": blockchain_topics[1]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Distributed ledger technology is a key blockchain concept that enables data to be stored and shared across multiple locations. It's a popular approach for building transparent and secure systems.",
        "author_id": users[0]['id'],
        "topic_id": blockchain_topics[1]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Distributed ledger technology is a critical aspect of modern blockchain. It's essential for enabling data to be stored and shared across multiple locations to build transparent and secure systems.",
        "author_id": users[1]['id'],
        "topic_id": blockchain_topics[1]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Smart contracts are self-executing contracts with the terms of the agreement between buyer and seller directly written into lines of code. They're a popular approach for automating and enforcing contract performance.",
        "author_id": users[2]['id'],
        "topic_id": blockchain_topics[2]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working with smart contracts, and I can say that they've helped me automate and enforce contract performance more effectively.",
        "author_id": users[3]['id'],
        "topic_id": blockchain_topics[2]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Smart contracts are self-executing contracts with the terms of the agreement between buyer and seller directly written into lines of code. They're a popular approach for automating and enforcing contract performance.",
        "author_id": users[0]['id'],
        "topic_id": blockchain_topics[2]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Smart contracts are a critical aspect of modern blockchain. They're essential for automating and enforcing contract performance by directly writing the terms of the agreement between buyer and seller into lines of code.",
        "author_id": users[1]['id'],
        "topic_id": blockchain_topics[2]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Consensus algorithms are key blockchain mechanisms for achieving agreement on a single data value among distributed processes or systems. They're a popular approach for ensuring the integrity and security of blockchain networks.",
        "author_id": users[2]['id'],
        "topic_id": blockchain_topics[3]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working with consensus algorithms, and I can say that they've helped me achieve agreement on data values more effectively.",
        "author_id": users[3]['id'],
        "topic_id": blockchain_topics[3]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Consensus algorithms are key blockchain mechanisms for achieving agreement on a single data value among distributed processes or systems. They're a popular approach for ensuring the integrity and security of blockchain networks.",
        "author_id": users[0]['id'],
        "topic_id": blockchain_topics[3]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Consensus algorithms are a critical aspect of modern blockchain. They're essential for achieving agreement on data values among distributed processes or systems to ensure the integrity and security of blockchain networks.",
        "author_id": users[1]['id'],
        "topic_id": blockchain_topics[3]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Blockchain scalability is a key challenge for blockchain networks to handle a large number of transactions and users. It's a popular area of research and development to improve the performance and efficiency of blockchain networks.",
        "author_id": users[2]['id'],
        "topic_id": blockchain_topics[4]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on blockchain scalability projects, and I can say that they've helped me improve the performance and efficiency of blockchain networks more effectively.",
        "author_id": users[3]['id'],
        "topic_id": blockchain_topics[4]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Blockchain scalability is a key challenge for blockchain networks to handle a large number of transactions and users. It's a popular area of research and development to improve the performance and efficiency of blockchain networks.",
        "author_id": users[0]['id'],
        "topic_id": blockchain_topics[4]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Blockchain scalability is a critical aspect of modern blockchain. It's essential for improving the performance and efficiency of blockchain networks to handle a large number of transactions and users.",
        "author_id": users[1]['id'],
        "topic_id": blockchain_topics[4]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Blockchain privacy is a key challenge for blockchain networks to protect the confidentiality and anonymity of users and transactions. It's a popular area of research and development to enhance the privacy and security of blockchain networks.",
        "author_id": users[2]['id'],
        "topic_id": blockchain_topics[5]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on blockchain privacy projects, and I can say that they've helped me enhance the privacy and security of blockchain networks more effectively.",
        "author_id": users[3]['id'],
        "topic_id": blockchain_topics[5]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Blockchain privacy is a key challenge for blockchain networks to protect the confidentiality and anonymity of users and transactions. It's a popular area of research and development to enhance the privacy and security of blockchain networks.",
        "author_id": users[0]['id'],
        "topic_id": blockchain_topics[5]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Blockchain privacy is a critical aspect of modern blockchain. It's essential for protecting the confidentiality and anonymity of users and transactions to enhance the privacy and security of blockchain networks.",
        "author_id": users[1]['id'],
        "topic_id": blockchain_topics[5]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Blockchain interoperability is a key challenge for blockchain networks to communicate and share data with other blockchain networks. It's a popular area of research and development to enable seamless interaction between different blockchain networks.",
        "author_id": users[2]['id'],
        "topic_id": blockchain_topics[6]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working on blockchain interoperability projects, and I can say that they've helped me enable seamless interaction between different blockchain networks more effectively.",
        "author_id": users[3]['id'],
        "topic_id": blockchain_topics[6]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Blockchain interoperability is a key challenge for blockchain networks to communicate and share data with other blockchain networks. It's a popular area of research and development to enable seamless interaction between different blockchain networks.",
        "author_id": users[0]['id'],
        "topic_id": blockchain_topics[6]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Blockchain interoperability is a critical aspect of modern blockchain. It's essential for enabling seamless interaction between different blockchain networks to communicate and share data with other blockchain networks.",
        "author_id": users[1]['id'],
        "topic_id": blockchain_topics[6]['id'],
        "created_at": ensure_valid_created_at(blockchain_topics[6]['created_at'])
    },
]


quantum_computing_replies = [
    {
        "id": uuid4(),
        "content": "Great topic! I've been learning about quantum computing and these concepts are really helpful.",
        "author_id": users[1]['id'],
        "topic_id": quantum_computing_topics[0]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I agree! Quantum computing is a critical field with a wide range of applications.",
        "author_id": users[2]['id'],
        "topic_id": quantum_computing_topics[0]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Thanks for sharing these insights! I'll keep them in mind as I continue to explore quantum computing.",
        "author_id": users[3]['id'],
        "topic_id": quantum_computing_topics[0]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Quantum computing is a rapidly growing field with many exciting opportunities. It's great to see more people getting interested in it.",
        "author_id": users[0]['id'],
        "topic_id": quantum_computing_topics[0]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "These concepts are essential for anyone looking to start a career in quantum computing. Thanks for sharing!",
        "author_id": users[1]['id'],
        "topic_id": quantum_computing_topics[0]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[0]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Quantum superposition is a key quantum computing concept that allows qubits to exist in multiple states simultaneously. It's a popular approach for performing multiple calculations at once.",
        "author_id": users[2]['id'],
        "topic_id": quantum_computing_topics[1]['id'],
        "created_at": ensure_valid_created_at
    },
    {
        "id": uuid4(),
        "content": "I've been working with quantum superposition, and I can say that it's helped me perform multiple calculations at once more effectively.",
        "author_id": users[3]['id'],
        "topic_id": quantum_computing_topics[1]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Quantum superposition is a key quantum computing concept that allows qubits to exist in multiple states simultaneously. It's a popular approach for performing multiple calculations at once.",
        "author_id": users[0]['id'],
        "topic_id": quantum_computing_topics[1]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Quantum superposition is a critical aspect of modern quantum computing. It's essential for allowing qubits to exist in multiple states simultaneously to perform multiple calculations at once.",
        "author_id": users[1]['id'],
        "topic_id": quantum_computing_topics[1]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[1]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Quantum entanglement is a key quantum computing concept that allows qubits to be correlated with each other regardless of the distance between them. It's a popular approach for creating secure communication channels.",
        "author_id": users[2]['id'],
        "topic_id": quantum_computing_topics[2]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working with quantum entanglement, and I can say that it's helped me create secure communication channels more effectively.",
        "author_id": users[3]['id'],
        "topic_id": quantum_computing_topics[2]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Quantum entanglement is a key quantum computing concept that allows qubits to be correlated with each other regardless of the distance between them. It's a popular approach for creating secure communication channels.",
        "author_id": users[0]['id'],
        "topic_id": quantum_computing_topics[2]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Quantum entanglement is a critical aspect of modern quantum computing. It's essential for allowing qubits to be correlated with each other regardless of the distance between them to create secure communication channels.",
        "author_id": users[1]['id'],
        "topic_id": quantum_computing_topics[2]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[2]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Quantum teleportation is a key quantum computing concept that allows qubits to be transferred between locations without physical movement. It's a popular approach for secure data transfer.",
        "author_id": users[2]['id'],
        "topic_id": quantum_computing_topics[3]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working with quantum teleportation, and I can say that it's helped me transfer qubits between locations without physical movement more effectively.",
        "author_id": users[3]['id'],
        "topic_id": quantum_computing_topics[3]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Quantum teleportation is a key quantum computing concept that allows qubits to be transferred between locations without physical movement. It's a popular approach for secure data transfer.",
        "author_id": users[0]['id'],
        "topic_id": quantum_computing_topics[3]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Quantum teleportation is a critical aspect of modern quantum computing. It's essential for allowing qubits to be transferred between locations without physical movement to secure data transfer.",
        "author_id": users[1]['id'],
        "topic_id": quantum_computing_topics[3]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[3]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Quantum cryptography is a key quantum computing concept that uses quantum mechanics to secure communication channels. It's a popular approach for protecting data from eavesdropping and interception.",
        "author_id": users[2]['id'],
        "topic_id": quantum_computing_topics[4]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working with quantum cryptography, and I can say that it's helped me secure communication channels more effectively.",
        "author_id": users[3]['id'],
        "topic_id": quantum_computing_topics[4]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Quantum cryptography is a key quantum computing concept that uses quantum mechanics to secure communication channels. It's a popular approach for protecting data from eavesdropping and interception.",
        "author_id": users[0]['id'],
        "topic_id": quantum_computing_topics[4]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Quantum cryptography is a critical aspect of modern quantum computing. It's essential for using quantum mechanics to secure communication channels and protect data from eavesdropping and interception.",
        "author_id": users[1]['id'],
        "topic_id": quantum_computing_topics[4]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[4]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Quantum error correction is a key quantum computing concept that uses quantum codes to detect and correct errors in quantum data. It's a popular approach for improving the reliability and accuracy of quantum computations.",
        "author_id": users[2]['id'],
        "topic_id": quantum_computing_topics[5]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working with quantum error correction, and I can say that it's helped me detect and correct errors in quantum data more effectively.",
        "author_id": users[3]['id'],
        "topic_id": quantum_computing_topics[5]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Quantum error correction is a key quantum computing concept that uses quantum codes to detect and correct errors in quantum data. It's a popular approach for improving the reliability and accuracy of quantum computations.",
        "author_id": users[0]['id'],
        "topic_id": quantum_computing_topics[5]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Quantum error correction is a critical aspect of modern quantum computing. It's essential for using quantum codes to detect and correct errors in quantum data to improve the reliability and accuracy of quantum computations.",
        "author_id": users[1]['id'],
        "topic_id": quantum_computing_topics[5]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[5]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Quantum algorithms are key quantum computing algorithms that leverage quantum mechanics to solve complex problems more efficiently than classical algorithms. They're a popular approach for achieving quantum speedup in computations.",
        "author_id": users[2]['id'],
        "topic_id": quantum_computing_topics[6]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "I've been working with quantum algorithms, and I can say that they've helped me solve complex problems more efficiently than classical algorithms.",
        "author_id": users[3]['id'],
        "topic_id": quantum_computing_topics[6]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Quantum algorithms are key quantum computing algorithms that leverage quantum mechanics to solve complex problems more efficiently than classical algorithms. They're a popular approach for achieving quantum speedup in computations.",
        "author_id": users[0]['id'],
        "topic_id": quantum_computing_topics[6]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Quantum algorithms are a critical aspect of modern quantum computing. They're essential for leveraging quantum mechanics to solve complex problems more efficiently than classical algorithms and achieve quantum speedup in computations.",
        "author_id": users[1]['id'],
        "topic_id": quantum_computing_topics[6]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[6]['created_at'])
    },
    {
        "id": uuid4(),
        "content": "Quantum machine learning is a key quantum computing application that uses quantum algorithms to enhance machine learning models. It's a popular approach for improving the performance and efficiency of machine learning tasks.",
        "author_id": users[2]['id'],
        "topic_id": quantum_computing_topics[6]['id'],
        "created_at": ensure_valid_created_at(quantum_computing_topics[7]['created_at'])
    },
]


conversations = [
    {
        "id": uuid4(),
        "created_at": random_date_within_last_month(),
        "user1_id": users[0]['id'],
        "user2_id": users[1]['id']
    },
    {
        "id": uuid4(),
        "created_at": random_date_within_last_month(),
        "user1_id": users[0]['id'],
        "user2_id": users[2]['id']
    },
    {
        "id": uuid4(),
        "created_at": random_date_within_last_month(),
        "user1_id": users[0]['id'],
        "user2_id": users[3]['id']
    },
    {
        "id": uuid4(),
        "created_at": random_date_within_last_month(),
        "user1_id": users[1]['id'],
        "user2_id": users[2]['id']
    },
    {
        "id": uuid4(),
        "created_at": random_date_within_last_month(),
        "user1_id": users[1]['id'],
        "user2_id": users[3]['id']
    },
    {
        "id": uuid4(),
        "created_at": random_date_within_last_month(),
        "user1_id": users[2]['id'],
        "user2_id": users[3]['id']
    },
]


messages = [
    {
        "id": uuid4(),
        "content": "Hey, how are you doing?",
        "author_id": users[0]['id'],
        "conversation_id": conversations[0]['id'],
        "created_at": datetime.now()
    },
    {
        "id": uuid4(),
        "content": "I'm good, thanks! How about you?",
        "author_id": users[1]['id'],
        "conversation_id": conversations[0]['id'],
        "created_at": datetime.now()
    },
    {
        "id": uuid4(),
        "content": "I'm doing great, thanks for asking!",
        "author_id": users[0]['id'],
        "conversation_id": conversations[0]['id'],
        "created_at": datetime.now()
    },
    {
        "id": uuid4(),
        "content": "Hey, how are you doing?",
        "author_id": users[0]['id'],
        "conversation_id": conversations[1]['id'],
        "created_at": datetime.now()
    },
    {
        "id": uuid4(),
        "content": "I'm good, thanks! How about you?",
        "author_id": users[2]['id'],
        "conversation_id": conversations[1]['id'],
        "created_at": datetime.now()
    },
    {
        "id": uuid4(),
        "content": "I'm doing great, thanks for asking!",
        "author_id": users[0]['id'],
        "conversation_id": conversations[1]['id'],
        "created_at": datetime.now()
    },
    {
        "id": uuid4(),
        "content": "Hey, how are you doing?",
        "author_id": users[0]['id'],
        "conversation_id": conversations[2]['id'],
        "created_at": datetime.now()
    },
    {
        "id": uuid4(),
        "content": "I'm good, thanks! How about you?",
        "author_id": users[3]['id'],
        "conversation_id": conversations[2]['id'],
        "created_at": datetime.now()
    },
    {
        "id": uuid4(),
        "content": "I'm doing great, thanks for asking!",
        "author_id": users[0]['id'],
        "conversation_id": conversations[2]['id'],
        "created_at": datetime.now()
    },
    {
        "id": uuid4(),
        "content": "Hey, how are you doing?",
        "author_id": users[1]['id'],
        "conversation_id": conversations[3]['id'],
        "created_at": datetime.now()
    },
    {
        "id": uuid4(),
        "content": "I'm good, thanks! How about you?",
        "author_id": users[2]['id'],
        "conversation_id": conversations[3]['id'],
        "created_at": datetime.now()
    },
    {
        "id": uuid4(),
        "content": "I'm doing great, thanks for asking!",
        "author_id": users[1]['id'],
        "conversation_id": conversations[3]['id'],
        "created_at": datetime.now()
    },
    {
        "id": uuid4(),
        "content": "Hey, how are you doing?",
        "author_id": users[1]['id'],
        "conversation_id": conversations[4]['id'],
        "created_at": datetime.now()
    },
    {
        "id": uuid4(),
        "content": "I'm good, thanks! How about you?",
        "author_id": users[3]['id'],
        "conversation_id": conversations[4]['id'],
        "created_at": datetime.now()
    },
    {
        "id": uuid4(),
        "content": "I'm doing great, thanks for asking!",
        "author_id": users[1]['id'],
        "conversation_id": conversations[4]['id'],
        "created_at": datetime.now()
    },
    {
        "id": uuid4(),
        "content": "Hey, how are you doing?",
        "author_id": users[2]['id'],
        "conversation_id": conversations[5]['id'],
        "created_at": datetime.now()
    },
    {
        "id": uuid4(),
        "content": "I'm good, thanks! How about you?",
        "author_id": users[3]['id'],
        "conversation_id": conversations[5]['id'],
        "created_at": datetime.now()
    },
    {
        "id": uuid4(),
        "content": "I'm doing great, thanks for asking!",
        "author_id": users[2]['id'],
        "conversation_id": conversations[5]['id'],
        "created_at": datetime.now()
    },
]


def insert_users(db: Session) -> None:
    for user in users:
        user = User(**user)
        db.add(user)

    db.commit()


def insert_admin(db: Session) -> None:
    for admin in admins:
        admin = Admin(**admin)
        db.add(admin)

    db.commit()


def insert_conversations(db: Session) -> None:
    for conversation in conversations:
        conversation = Conversation(**conversation)
        db.add(conversation)

    db.commit()


def insert_messages(db: Session) -> None:
    for message in messages:
        message = Message(**message)
        db.add(message)

    db.commit()


def insert_categories(db: Session) -> None:
    for category in categories:
        category = Category(**category)
        db.add(category)

    db.commit()


def insert_topics(db: Session) -> None:
    topics = sorted(
        [
            *programming_topics, 
            *data_science_topics, 
            *ai_topics, 
            *cybersecurity_topics, 
            *software_engineering_topics,
            *computer_networks_topics, 
            *ml_topics,
            *cloud_computing_topics, 
            *blockchain_topics, 
            *quantum_computing_topics
        ], 
        key=lambda x: x['created_at']
    )

    for topic in topics:
        topic = Topic(**topic)
        db.add(topic)

    db.commit()


replies = [
    *programming_replies, 
    *data_science_replies, 
    *artificial_intelligence_replies, 
    *cybersecurity_replies, 
    *software_engineering_replies,
    *computer_networks_replies, 
    *machine_learning_replies,
    *cloud_computing_replies, 
    *blockchain_replies, 
    *quantum_computing_replies
]


def insert_replies(db: Session) -> None:
    sorted_replies = sorted(replies, key=lambda x: x['created_at'])

    for reply in sorted_replies:
        reply = Reply(**reply)
        db.add(reply)

    db.commit()


def insert_reply_reactions(db: Session) -> None:
    user_indexes = list(range(len(users)))

    for reply in replies:
        selected_user_indexes = random.sample(
            user_indexes, 
            random.randrange(0, len(user_indexes) + 1)
        )
        for user_idx in selected_user_indexes:
            reply_reaction = ReplyReaction(
                user_id=users[user_idx]['id'],
                reply_id=reply['id'],
                reaction=random.choices((True, False), weights=[80, 20], k=1)[0], 
                created_at=ensure_valid_created_at(reply['created_at'])
            )
            db.add(reply_reaction)

    db.commit()


def insert_user_category_permissions(db: Session) -> None:
    user_indexes = list(range(len(users)))

    for category in categories:
        selected_user_indexes = random.sample(
            user_indexes, 
            random.randrange(1, len(user_indexes) + 1)
        )
        for user_idx in selected_user_indexes:
            user_category_permission = UserCategoryPermission(
                user_id=users[user_idx]['id'],
                category_id=category['id'], 
                access_level=random.choices(
                    (AccessLevel.READ, AccessLevel.WRITE), 
                    weights=[75, 25], 
                    k=1
                )[0]
            )
            db.add(user_category_permission)

    db.commit()


def insert_init_data(db: Session) -> None:
    insert_users(db)
    insert_admin(db)
    insert_categories(db)
    insert_user_category_permissions(db)
    insert_topics(db)
    insert_replies(db)
    insert_reply_reactions(db)
    insert_conversations(db)
    insert_messages(db)
