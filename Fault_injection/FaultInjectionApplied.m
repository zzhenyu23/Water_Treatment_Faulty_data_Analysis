% Inject faults
% example using bsm1rainyr2
data = bsm1rainyr2;
time = bsm1rainyr2.Timedays;

% Define faults
faults(1).variable = 'S_O';
faults(1).type = 'bias';
faults(1).param.offset = 0.1;
faults(1).t_start = 4;
faults(1).t_end = 4.1;

faults(2).variable = 'S_O';
faults(2).type = 'drift';
faults(2).param.slope = 0.001;
faults(2).t_start = 4.5;
faults(2).t_end = 4.8;

faults(3).variable = 'S_O';
faults(3).type = 'dropout';
faults(3).param.freq = 0.1;
faults(3).t_start = 7;
faults(3).t_end = 7.1;

faults(4).variable = 'S_O';
faults(4).type = 'spike';
faults(4).param.freq = 0.05;
faults(4).param.magnitude = 0.2;
faults(4).t_start = 4.1;
faults(4).t_end = 4.11;

faults(5).variable = 'S_O';
faults(5).type = 'noise';
faults(5).param.magnitude = 0.2;
faults(5).t_start = 5;
faults(5).t_end = 5.09;

faults(6).variable = 'S_O';
faults(6).type = 'scaling';
faults(6).param.factor = 1.11;
faults(6).t_start = 7.9;
faults(6).t_end = 8;

faults(7).variable = 'S_O';
faults(7).type = 'stuck';
faults(7).t_start = 7.7;
faults(7).t_end = 7.9;


% Inject faults
[data_faulty, fault_log] = inject_faults(data, time, faults);

% Display fault log
disp(fault_log);

% Optional: plot original vs faulty
figure;
plot(time, data.S_O, 'b', time, data_faulty.S_O, 'r--');
legend('Original','Faulty'); title('S_O');
