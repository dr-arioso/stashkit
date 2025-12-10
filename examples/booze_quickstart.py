from stashkit import use_booster_pack

def main():
    booze = use_booster_pack("BoozeDex")
    entity = booze.resolve("photo-of-bottle.jpg")
    print(entity)

if __name__ == '__main__':
    main()
