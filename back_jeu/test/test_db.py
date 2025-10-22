from src.db.app import (
    add_performance,
    get_db,
    get_performances,
    remove_performance,
    update_performance,
)

# NOTE: Absolute path here is normal

def test_add_remove_performance():
    db_gen = get_db()
    db = next(db_gen)
    performance = add_performance(db, name="ToRemove", time_taken=5678)
    assert performance.id is not None
    assert performance.name == "ToRemove"
    assert performance.time_taken == 5678
    result = remove_performance(db, performance.id)
    assert result is True
    result = remove_performance(db, 99999)  # Non-existent ID
    assert result is False
    db_gen.close()

def test_update_performance():
    db_gen = get_db()
    db = next(db_gen)
    performance = add_performance(db, name="ToUpdate", time_taken=1234)
    assert performance.id is not None
    assert performance.name == "ToUpdate"
    assert performance.time_taken == 1234
    updated_performance = update_performance(
        db, performance.id, name="UpdatedName", time_taken=4321
    )
    assert updated_performance is not None
    assert updated_performance.name == "UpdatedName"
    assert updated_performance.time_taken == 4321
    result = update_performance(db, 99999, name="Nope")  # Non-existent ID
    assert result is None
    result = remove_performance(db, performance.id)
    assert result is True
    db_gen.close()
