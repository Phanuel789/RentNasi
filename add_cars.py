from app import app, db, Car

with app.app_context():
    db.create_all()

    cars = [
        Car(name="Toyota Land Cruiser", image="toyota_land_cruiser.jpg", rate=3500),
        Car(name="Range Rover", image="range_rover.jpg", rate=4000),
        Car(name="BMW X5", image="bmw_x5.jpg", rate=3000),
        Car(name="Mercedes-Benz G-Class", image="mercedes_g_class.jpg", rate=4500),
        Car(name="Audi Q7", image="audi_q7.jpg", rate=3200),
        Car(name="Lexus LX", image="lexus_lx.jpg", rate=3400),
        Car(name="Jeep Wrangler", image="jeep_wrangler.jpg", rate=3100),
        Car(name="Ford Mustang", image="ford_mustang.jpg", rate=3800),
        Car(name="Chevrolet Camaro", image="chevrolet_camaro.jpg", rate=3600),
        Car(name="Nissan Patrol", image="nissan_patrol.jpg", rate=2900),
        Car(name="Honda CR-V", image="honda_crv.jpg", rate=2500),
        Car(name="Hyundai Tucson", image="hyundai_tucson.jpg", rate=2400),
        Car(name="Volkswagen Tiguan", image="volkswagen_tiguan.jpg", rate=2300),
        Car(name="Kia Sportage", image="kia_sportage.jpg", rate=2200),
        Car(name="Maserati Levante", image="maserati_levante.jpg", rate=3700),
        Car(name="Ferrari Portofino", image="ferrari_portofino.jpg", rate=6000),
        Car(name="Lamborghini Urus", image="lamborghini_urus.jpg", rate=6500),
        Car(name="Bentley Bentayga", image="bentley_bentayga.jpg", rate=6200),
        Car(name="Rolls-Royce Cullinan", image="rolls_royce_cullinan.jpg", rate=7000),
        Car(name="Aston Martin DBX", image="aston_martin_dbx.jpg", rate=5800),
        Car(name="Bugatti Chiron", image="bugatti_chiron.jpg", rate=9000),
        Car(name="McLaren 720S", image="mclaren_720s.jpg", rate=8500)
    ]

    db.session.add_all(cars)
    db.session.commit()

    print("✅ Successfully added 22 cars to the database!")
