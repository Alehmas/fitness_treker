from dataclasses import dataclass
from typing import ClassVar, List


@dataclass
class InfoMessage:
    """Informational message about the workout."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return (f'Workout type: {self.training_type}; '
                f'Duration: {self.duration:.3f} h.;'
                f'Distance: {self.distance:.3f} km;'
                f'Average speed: {self.speed:.3f} kph;'
                f'Сalories burned: {self.calories:.3f}.')


@dataclass
class Training:
    """Base training class."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MINS_IN_HOUR: ClassVar[int] = 60
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Get distance in km."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Get average moving speed."""
        speed_average = self.get_distance() / self.duration
        return speed_average

    def get_spent_calories(self) -> float:
        """Get calories burned."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Return an informational message about the completed workout."""
        message = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return message


class Running(Training):
    """Workout: running."""
    coeff_calorie_1: ClassVar[int] = 18
    coeff_calorie_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        spent_calories = ((self.coeff_calorie_1 * self.get_mean_speed()
                           - self.coeff_calorie_2) * self.weight / self.M_IN_KM
                          * self.duration * self.MINS_IN_HOUR)
        return spent_calories


@dataclass
class SportsWalking(Training):
    """Training: sportive walking."""
    coeff_calorie_1: ClassVar[float] = 0.035
    coeff_calorie_2: ClassVar[int] = 2
    coeff_calorie_3: ClassVar[float] = 0.029
    height: int

    def get_spent_calories(self) -> float:
        time_training = self.duration * self.MINS_IN_HOUR
        spent_calories = ((self.coeff_calorie_1 * self.weight
                           + (self.get_mean_speed() ** self.coeff_calorie_2
                              // self.height) * self.coeff_calorie_3
                           * self.weight) * time_training)
        return spent_calories


@dataclass
class Swimming(Training):
    """Training: swimming."""
    LEN_STEP: ClassVar[float] = 1.38
    coeff_calorie_1: ClassVar[float] = 1.1
    coeff_calorie_2: ClassVar[int] = 2
    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Get the average speed of movement."""
        speed_average = (self.count_pool * self.length_pool / self.M_IN_KM
                         / self.duration)
        return speed_average

    def get_spent_calories(self) -> float:
        spent_calories = ((self.get_mean_speed() + self.coeff_calorie_1)
                          * self.coeff_calorie_2 * self.weight)

        return spent_calories


def read_package(workout_type: str, data: List[int]) -> Training:
    """Read the data received from the sensors."""
    codes_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    try:
        type_training = codes_dict[workout_type](*data)
        return type_training
    except (AttributeError, KeyError):
        raise ValueError('Wrong training')


def main(training: Training) -> None:
    """Main function."""
    info = training.show_training_info()
    message = info.get_message()
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
