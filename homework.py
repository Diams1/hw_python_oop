from typing import Dict, Type
from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    string_ru: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Вывод сообщения о тренировке"""
        message: str = self.string_ru.format(**asdict(self))
        return message


class Training:
    """Базовый класс тренировки."""
    COEF_CCAL_1: int = 18
    COEF_CCAL_2: int = 20
    MIN_IN_HOUR: int = 60
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_meters: float = self.action * self.LEN_STEP
        distance: float = distance_meters / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_speed: float = self.get_distance() / self.duration
        return avg_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'В классе {self.__class__.__name__} '
            'не определён метод <get_spent_calories>!')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_info = InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories())
        return training_info


class Running(Training):
    """Тренировка: бег."""
    COEF_CALORIE_1: int = 18
    COEF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_min: float = self.duration * self.MIN_IN_HOUR
        calc_speed_coef: float = self.COEF_CALORIE_1 * self.get_mean_speed()
        calc_avg_speed: float = (
            calc_speed_coef - self.COEF_CALORIE_2) * self.weight
        spent_calories: float = calc_avg_speed / self.M_IN_KM * duration_min
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029
    COEFF_SQUARE: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_min: float = self.duration * self.MIN_IN_HOUR
        calc_formula: float = (
            self.get_mean_speed() ** self.COEFF_SQUARE // self.height)
        calc_weight_coef1: float = self.COEFF_CALORIE_1 * self.weight
        calc_weight_coef2: float = self.COEFF_CALORIE_2 * self.weight
        spent_calories: float = (
            (calc_weight_coef1 + calc_formula
             * calc_weight_coef2) * duration_min)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEF_SWM: int = 2
    COEF_CALORIE: float = 1.1

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плавания."""
        distance_meters: int = self.length_pool * self.count_pool
        distance_km: float = distance_meters / self.M_IN_KM
        avg_speed: float = distance_km / self.duration
        return avg_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coef_speed: float = self.get_mean_speed() + self.COEF_CALORIE
        coef_swim: float = coef_speed * self.COEF_SWM
        spent_calories: float = coef_swim * self.weight
        return spent_calories


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    traning_types: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in traning_types:
        raise ValueError(f'{workout_type} - неизвестный тип тренировки.')
    return traning_types[workout_type](*data)


def main(training: Type[Training]) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
