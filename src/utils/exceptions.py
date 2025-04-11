from fastapi import HTTPException, status

# Just an exceptions file

invalid_credentials_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password"
)

email_already_registered_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
)

username_already_registered_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered"
)

no_changes_provided_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="No changes provided"
)

user_is_max_rank_exception = HTTPException(
    status.HTTP_400_BAD_REQUEST, {"message": "User is already at max rank"}
)

user_is_min_rank_exception = HTTPException(
    status.HTTP_400_BAD_REQUEST, {"message": "User is already at min rank"}
)

not_enough_funds_exception = HTTPException(
    status.HTTP_400_BAD_REQUEST, {"message": "Not enough funds"}
)

too_small_funds_value_exception = HTTPException(
    status.HTTP_400_BAD_REQUEST, {"message": "You must provide a value greater than your current profit"}
)

lets_find_withdraw_solution_exception = HTTPException(
    status.HTTP_400_BAD_REQUEST, {"message": "We don't have enough money right now, lets find solution"}
)

user_withdraw_less_than_min_value_exception = HTTPException(
    status.HTTP_400_BAD_REQUEST, {"message": "Your balance is less than minimum value, you can withdraw only all funds"}
)

invalid_token_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
)

user_not_admin_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="User is not an admin"
)

user_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
)

trade_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Trade not found"
)

operation_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Operation not found"
)
