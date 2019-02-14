from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import base, Catalog, CatalogItem, User
engine = create_engine('sqlite:///catalogitem.db')
base.metadata.create_all(engine)
DBsession = sessionmaker(bind=engine)

session = DBsession()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

catalog1 = Catalog(name='Home', user_id=1)
session.add(catalog1)
session.commit()

catalog2 = Catalog(name='Technology', user_id=1)
session.add(catalog2)
session.commit()

# add items of it
item1 = CatalogItem(user_id=1, title='Medicine',
                    description='Medicine is the science and practice' /
                                '  of establishing the diagnosis,' /
                                'prognosis,treatment, and prevention' /
                                'of disease. Medicine encompasses a variety ' /
                                ' of health care practices evolved to  ' /
                                'maintain and restore health' /
                                'by the prevention and treatment of illness' /
                                '. Contemporary medicine applies biomedical ' /
                                'sciences, b iomedical research,' /
                                ' genetics, and medical technology to ' /
                                ' diagnose, treat, and prevent injury and' /
                                ' disease, typically through pharmaceuticals' /
                                ' or surgery, but also through' /
                                ' therapies as diverse as psychotherapy, ' /
                                '  external splints and traction, medical' /
                                ' devices, biologics, and ionizing radiation' /
                                ' amongst others.[1]',
                    catalog=catalog2, category='Technology')
session.add(item1)
session.commit()

item2 = CatalogItem(user_id=1, title='Robot',
                    description='ussing robot in all fields',
                    catalog=catalog2, category='Technology')
session.add(item2)
session.commit()

item3 = CatalogItem(user_id=1, title='programming ',
                    description='learn how to learn and apply programming ' /
                                'in every filed as medicine,and all fields',
                    catalog=catalog2, category='Technology')
session.add(item3)
session.commit()

item4 = CatalogItem(user_id=1, title=' netflex',
                    description='learn how to learn and apply programming' /
                                ' in every filed as medicine,and all fields',
                    catalog=catalog2, category='Technology')
session.add(item4)
session.commit()

item5 = CatalogItem(user_id=1, title='how to convert word to pdf ',
                    description='learn how to convert word to pdf',
                    catalog=catalog2, category='Technology')
session.add(item5)
session.commit()


catalog3 = Catalog(name='Art', user_id=1)
session.add(catalog3)
session.commit()

item1 = CatalogItem(user_id=1, title='the most beautiful films in 90 minute ',
                    description='watch films and not be boring in 90 minute',
                    catalog=catalog3, category='Art')
session.add(item1)
session.commit()

item2 = CatalogItem(user_id=1, title='Music ',
                    description='5 question you need to ask them' /
                                ' to music of the street',
                    catalog=catalog3, category='Art')
session.add(item2)
session.commit()


catalog4 = Catalog(user_id=1, name='Education')
session.add(catalog4)
session.commit()

item1 = CatalogItem(user_id=1, title='Scolarships',
                    description='to complete your education' /
                                'in a different country',
                    catalog=catalog4, category='Education')
session.add(item1)
session.commit()

item2 = CatalogItem(user_id=1, title='Types Of Education',
                    description='There are 4 types  what one you have',
                    catalog=catalog4, category='Education')
session.add(item2)
session.commit()


catalog5 = Catalog(name='Biography', user_id=1)
session.add(catalog5)
session.commit()

item1 = CatalogItem(user_id=1, title='biography of taha hussein',
                    description='read and learn from this',
                    catalog=catalog5, category='Biography')
session.add(item1)
session.commit()

item2 = CatalogItem(user_id=1, title='biography of woody',
                    description='funny character &&&&&&&&&&&& ',
                    catalog=catalog5, category='Biography')
session.add(item2)
session.commit()

catalog6 = Catalog(name='Blogs', user_id=1)
session.add(catalog6)
session.commit()

item1 = CatalogItem(user_id=1, title='we can not be friends one day ',
                    description='read and learn from this',
                    catalog=catalog6,  category='Blogs')
session.add(item1)
session.commit()

item2 = CatalogItem(user_id=1, title='where was my day',
                    description='all my previous days went in what and where ',
                    catalog=catalog6, category='Blogs')
session.add(item2)
session.commit()

catalog7 = Catalog(user_id=1, name='Books')
session.add(catalog7)
session.commit()

item1 = CatalogItem(user_id=1, title='political',
                    description='read and learn from this',
                    catalog=catalog7, category='Books')
session.add(item1)
session.commit()

item2 = CatalogItem(user_id=1, title='religious',
                    description='read and learn from this ',
                    catalog=catalog7, category='Books')
session.add(item2)
session.commit()

catalog8 = Catalog(user_id=1, name='cinema')
session.add(catalog8)
session.commit()

item1 = CatalogItem(user_id=1, title='fantasia ',
                    description='watch and enjoy',
                    catalog=catalog8, category='cinema')
session.add(item1)
session.commit()

item2 = CatalogItem(user_id=1, title='funny',
                    description='watch and laugh ',
                    catalog=catalog8, category='cinema')
session.add(item2)
session.commit()

catalog9 = Catalog(name='mathematics', user_id=1)
session.add(catalog9)
session.commit()

item1 = CatalogItem(user_id=1, title='how to memory multiplication ',
                    description='how to memory multiplication',
                    catalog=catalog9, category='mathematics')
session.commit()

item2 = CatalogItem(user_id=1, title='summation',
                    description='read and learn from this ',
                    catalog=catalog9, category='mathematics')
session.add(item2)
session.commit()


catalog10 = Catalog(user_id=1, name='Travel')
session.add(catalog1)
session.commit()


item1 = CatalogItem(user_id=1, title='countries ',
                    description='know about countries ',
                    catalog=catalog10, category='travel')
session.add(item1)
session.commit()

item2 = CatalogItem(user_id=1, title='how to travel from one country to',
                    description='how to travel from one country to another',
                    catalog=catalog10, category='travel')
session.add(item2)
session.commit()

print "added menu items!"
