import flatbuffers
from MyGame.Sample import Monster, Vec3, Weapon, Color, Equipment

# Builder for our Monster
builder = flatbuffers.Builder(1024)

# Create weapon names
sword_name = builder.CreateString("Sword")
axe_name = builder.CreateString("Axe")

# Create Weapons
Weapon.WeaponStart(builder)
Weapon.WeaponAddName(builder, sword_name)
Weapon.WeaponAddDamage(builder, 10)
sword = Weapon.WeaponEnd(builder)

Weapon.WeaponStart(builder)
Weapon.WeaponAddName(builder, axe_name)
Weapon.WeaponAddDamage(builder, 15)
axe = Weapon.WeaponEnd(builder)

# Create weapons vector
Monster.MonsterStartWeaponsVector(builder, 2)
builder.PrependUOffsetTRelative(axe)
builder.PrependUOffsetTRelative(sword)
weapons = builder.EndVector(2)

# Create inventory vector (e.g. bytes from 0 to 9)
inventory_data = [i for i in range(10)]
Monster.MonsterStartInventoryVector(builder, len(inventory_data))
for byte in reversed(inventory_data):
    builder.PrependByte(byte)
inventory = builder.EndVector(len(inventory_data))

# Create path (vector of Vec3)
Monster.MonsterStartPathVector(builder, 2)
v2 = Vec3.CreateVec3(builder, 4.0, 5.0, 6.0)
v1 = Vec3.CreateVec3(builder, 1.0, 2.0, 3.0)
path = builder.EndVector(2)

# Create name
name = builder.CreateString("Orc")

# Create position
Vec3.CreateVec3(builder, 1.0, 2.0, 3.0)
position = Vec3.CreateVec3(builder, 1.0, 2.0, 3.0)

# Start the Monster table
Monster.MonsterStart(builder)
Monster.MonsterAddPos(builder, position)
Monster.MonsterAddHp(builder, 80)
Monster.MonsterAddName(builder, name)
Monster.MonsterAddInventory(builder, inventory)
Monster.MonsterAddColor(builder, Color.Color().Red)
Monster.MonsterAddWeapons(builder, weapons)
Monster.MonsterAddEquippedType(builder, Equipment.Equipment().Weapon)
Monster.MonsterAddEquipped(builder, sword)
Monster.MonsterAddPath(builder, path)
orc = Monster.MonsterEnd(builder)

# Finish
builder.Finish(orc)
buf = builder.Output()

# Deserialize
monster = Monster.Monster.GetRootAsMonster(buf, 0)
print("Monster name:", monster.Name().decode("utf-8"))
print("HP:", monster.Hp())
print("Inventory:", [monster.Inventory(i) for i in range(monster.InventoryLength())])
print("Weapons:")
for i in range(monster.WeaponsLength()):
    w = monster.Weapons(i)
    print(f"  - {w.Name().decode('utf-8')} (Damage: {w.Damage()})")
