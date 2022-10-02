import loc_to_weather as ltw
import get_loc_data as gld

if __name__ == "__main__":
    gld.locnames_to_data()
    ltw.loc_to_weather()
