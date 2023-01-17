import majDB
import restaurantData
import cultureData
import spectacleData

if __name__=="__main__":
    majDB.dropTable()
    majDB.initActivity()
    majDB.initRestaurant()
    majDB.initSpectacle()
    restaurantData.main()
    cultureData.main()
    spectacleData.main()