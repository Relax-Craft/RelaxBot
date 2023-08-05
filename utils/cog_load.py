import os

def load_cogs(bot):
    for x in os.listdir("./extensions"):
        if x.endswith(".py"):
            bot.load_extension(f"extensions.{x[:-3]}")
            print(x)

        elif "." in x:
            continue

        else:
            print(x)
            for y in os.listdir(f"./extensions/{x}"):
                if y.endswith(".py"):
                    bot.load_extension(f"extensions.{x}.{y[:-3]}")
                    print(f"  {y}")
        print("")