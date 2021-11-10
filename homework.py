from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed_average = self.get_distance() / self.duration
        return speed_average

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20
    coeff_calorie_3 = 60

    def get_spent_calories(self) -> float:
        spent_calories = ((self.coeff_calorie_1 * self.get_mean_speed()
                           - self.coeff_calorie_2) * self.weight / self.M_IN_KM
                          * self.duration * self.coeff_calorie_3)
        return spent_calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_1 = 0.035
    coeff_calorie_2 = 2
    coeff_calorie_3 = 60
    coeff_calorie_4 = 0.029
    action: int
    duration: float
    weight: float
    height: int

    def get_spent_calories(self) -> float:
        time_training = self.duration * self.coeff_calorie_3
        spent_calories = ((self.coeff_calorie_1 * self.weight
                           + (self.get_mean_speed() ** self.coeff_calorie_2
                              // self.height) * self.coeff_calorie_4
                           * self.weight) * time_training)
        return spent_calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    coeff_calorie_1 = 1.1
    coeff_calorie_2 = 2
    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed_average = (self.count_pool * self.length_pool / self.M_IN_KM
                         / self.duration)
        return speed_average

    def get_spent_calories(self) -> float:
        spent_calories = ((self.get_mean_speed() + self.coeff_calorie_1)
                          * self.coeff_calorie_2 * self.weight)

        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    codes_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    try:
        type_training = codes_dict[workout_type](*data)
        return type_training
    except (AttributeError, KeyError):
        print('Wrong training')
        raise


def main(training: Training) -> None:
    """Главная функция."""
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
