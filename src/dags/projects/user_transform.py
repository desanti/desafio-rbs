import pandas as pd


class UserTransform:
    @staticmethod
    def transform(df: pd.DataFrame) -> pd.DataFrame:
        df[["title_name", "firstname", "lastname"]] = pd.DataFrame(df["name"].tolist())

        df = pd.concat([df, UserTransform._transform_location(df)], axis=1)

        df[["date_of_birth"]] = pd.DataFrame(df["dob"].tolist(), columns=["date"])
        df[["registered_date"]] = pd.DataFrame(df["registered"].tolist(), columns=["date"])

        df = UserTransform._clean_data(df)

        df = UserTransform._set_dtype(df)

        return df

    @staticmethod
    def _transform_location(df: pd.DataFrame) -> pd.DataFrame:
        df_location = pd.DataFrame(df["location"].tolist())
        df_location[["street_number", "street_name"]] = pd.DataFrame(df_location["street"].tolist())
        df_location[["latitude", "longitude"]] = pd.DataFrame(df_location["coordinates"].tolist())
        df_location[["tz_offset", "tz_description"]] = pd.DataFrame(df_location["timezone"].tolist())

        return df_location

    @staticmethod
    def _clean_data(df: pd.DataFrame) -> pd.DataFrame:
        columns = [
            "title_name",
            "firstname",
            "lastname",
            "gender",
            "street_name",
            "street_number",
            "city",
            "state",
            "country",
            "postcode",
            "latitude",
            "longitude",
            "tz_offset",
            "tz_description",
            "date_of_birth",
            "email",
            "phone",
            "cell",
            "nat",
            "registered_date"
        ]

        return df[columns]

    @staticmethod
    def _set_dtype(df: pd.DataFrame) -> pd.DataFrame:
        mapping = {
            "title_name": "str",
            "firstname": "str",
            "lastname": "str",
            "gender": "str",
            "street_name": "str",
            "street_number": "int",
            "city": "str",
            "state": "str",
            "country": "str",
            "postcode": "str",
            "latitude": "str",
            "longitude": "str",
            "tz_offset": "str",
            "tz_description": "str",
            "date_of_birth": "datetime64",
            "email": "str",
            "phone": "str",
            "cell": "str",
            "nat": "str",
            "registered_date": "datetime64",
        }

        return df.astype(mapping)
