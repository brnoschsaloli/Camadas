import numpy as np
import matplotlib.pyplot as plt

# Amostras do sinal AM modulado
sample_rate = 1000  # Taxa de amostragem
duration = 1.0  # Duração do sinal em segundos
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
carrier_frequency = 10  # Frequência da portadora em Hz
message_frequency = 2  # Frequência do sinal de áudio em Hz
amplitude = 1.0  # Amplitude do sinal de áudio

# Sinal de áudio original
message_signal = amplitude * np.sin(2 * np.pi * message_frequency * t)

# Sinal modulado
modulated_signal = (1 + 0.5 * message_signal) * np.sin(2 * np.pi * carrier_frequency * t)

# Demodulação: Detector de envoltória
envelope_signal = np.abs(modulated_signal)


# Plote os sinais para visualização
plt.figure(figsize=(10, 6))
plt.subplot(3, 1, 1)
plt.plot(t, message_signal)
plt.title('Sinal de Áudio Original')
plt.subplot(3, 1, 2)
plt.plot(t, modulated_signal)
plt.title('Sinal AM Modulado')
plt.subplot(3, 1, 3)
plt.plot(t, envelope_signal)
plt.title('Sinal da Envoltória (Demodulado)')
plt.tight_layout()
plt.show()
