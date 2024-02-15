# Training Generator

Database with different exercises
sqlite3 Database is used
Info on how to use it https://www.tutorialspoint.com/sqlite/sqlite_create_database.htm

# Database structure:

Columns:
Exercise name - The exercise should have an easy to identify name //
Description text - should describe the exercise
Description link - Link to picture or video
Skill level - all, kids, normal, rambo, senior, beginners
Type of training - warming up, game, strength, stretching, balance, reaction
Body part - legs, upper body, shoulder and arms
Equipment needed - 1 soft-ball, several soft-balls, bean bags, pistarit, tennis balls, stretching band
Amount of persons - 1,2,3,4,5,6,7,8 or more
Not suitable for - knees, back, breast, hip, neck, ankle
Duratation - x minutes
 

# Intended usage:
User choose from dropdown menu:
age, type, body part, equipment need, amount of persons, not suitable for
This is repeated till he says "enough exercises" (age is cached)
Outcome: Training plan, sorting for warming up, main training, in-between games, flexing

# Additional planned features
Adding of exercises
Modification of entries in the database
Modification of received trainings plan
