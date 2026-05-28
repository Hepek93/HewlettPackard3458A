import pyvisa
import time

class HP3458A:
    """Class that controls HP3458A.
    """
    
    def __init__(self, dev_info, read_termination = '\r\n', write_termination = '\r\n', delay = 0.05, timeout = 10_000) -> None:
        """Constructor

        Args:
            dev_info (str): GPIB connection e.g. ['GPIB0::22::INSTR'])
            read_termination (str, optional): Read termination. Defaults to '\\r\\n'.
            write_termination (str, optional): Write termination. Defaults to '\\r\\n'.
            delay (float, optional): Delay between two commands. Defaults to 0.05.
            timeout (int, optional): VISA timeout. Defaults to 10_000.
        """
        self.__instrument_connected = False
        
        rm = pyvisa.ResourceManager()
        try:
            self.__inst = rm.open_resource(dev_info, write_termination=write_termination, read_termination=read_termination)
            self.__instrument_connected = True
            self.__inst.timeout = timeout
            self.__delay = delay
        except:
            print('Check connection with HP3458A')
    
    def __get_data(self,query) -> str:
        if self.__instrument_connected:
            try:
                recv = self.__inst.query(query)
                time.sleep(self.__delay)
                return recv
            except:
                print('Can not query data from the HP3458A')
            
        else:
            print('HP3458A is not connected')
        return None

    def __write_data(self, data) -> bool:
        if self.__instrument_connected:
            try:
                self.__inst.write(data)
                time.sleep(self.__delay)
                return True
            except Exception as e: 
                print('Can not send data to the HP3458A')
                print('Reason:', e)
            
        else:
            print('HP3458A is not connected')
        return False

    def close_connection(self) -> None:
        """Close connection
        """
        if self.__instrument_connected:
            self.__inst.close()
            self.__instrument_connected = False

    def get_id(self) -> str:
        """The multimeter responds to the ID? command by sending the
        string "Keysight 3458A". This feature allows the GPIB controller to locate the
        multimeter by its address.

        Returns:
            str: info
        """
        return self.__get_data('ID?')
    
    
    def set_aperture(self, aper = 500E-9) -> bool:
        """Specifies the A/D converter integration time in seconds.

        Args:
            aper (int, str): Specifies the A/D converter's integration time and overrides any previously
            specified integration time or resolution. The valid range for aperture is 0 - 1 s in
            increments of 100 ns. (Specifying a value <500 ns selects minimum aperture
            which is 500 ns.)
            Default aperture = 500 ns.
            Remarks:
            Since the APER and NPLC commands both set the integration time, executing
            either will cancel the integration time previously established by the other. The
            RES command or the %_resolution parameter of a function or RANGE
            command can also be used to indirectly select an integration time. An
            interaction occurs between APER (or NPLC) when you specify resolution as
            follows:
                - If you send the APER (or NPLC) command before specifying resolution, the
                multimeter satisfies the command that specifies greater resolution (more
                integration time).
                - If you send the APER (or NPLC) command after specifying resolution, the
                multimeter uses the integration time specified by the APER (or NPLC)
                command, and any previously specified resolution is ignored.

        Returns:
            bool: status
        """
        try:
            aper = float(aper)
            if aper<=1 and aper>=500E-9:
                return self.__write_data(f'APER {aper}')
            else:
                return False
        except ValueError:
            return False
        
    def get_aperture(self) -> str:
        """Returns the currently specified integration time (in seconds) used by the A/D converter.

        Returns:
            str: aperture time.
        """
        return self.__get_data(f'APER?')
    
    def set_autorange(self, state = 'ON') -> bool:
        """Autorange. Enables or disables the autorange function.

        Args:
            state (str, optional): ON, OFF or ONCE (Causes the multimeter to autorange once, then disables
            autoranging). Defaults to 'ON'.
            Remarks:
            - With autorange enabled, the multimeter samples the input signal before each
            reading and selects the appropriate range.
            - Autorange does not operate for direct- or sub-sampled measurements (DSAC,
            DSDC, SSAC, or SSDC command) or when using the TIMER sample event or
            the SWEEP command.

        Returns:
            bool: status
        """
        if state == 'ON' or state == 'OFF':
            return self.__write_data(f'ARANGE {state}')
        else:
            return False
        
    def get_autorange(self) -> str:
        """Returns the current autorange setting.

        Returns:
            str: ON, OFF or ONCE
        """
        return self.__get_data(f'ARANGE?')
    
    def set_autozero(self, state = 'ON') -> bool:
        """Enables or disables the autozero function. The autozero function
            applies only to DC voltage, DC current, and resistance measurements.

        Args:
            state (str, optional): ON (Zero measurement is updated after every measurement), OFF (Zero measurement is updated once, then only after a function,
            range, aperture, NPLC, or resolution change.) or ONCE (Zero measurement is updated once, then only after a function,
            range, aperture, NPLC, or resolution change.). Defaults to 'ON'.
            Remarks:
            - When autozero is ON, the multimeter makes a zero measurement
            (measurement with the input disabled) following every reading and
            algebraically subtracts the zero measurement from the reading. This
            approximately doubles the time required per reading.\n
            - Notice that the control parameters OFF and ONCE have the same effect. When
            autozero is OFF or ONCE, the multimeter makes one zero measurement and
            algebraically subtracts this from subsequent readings. After you execute
            AZERO OFF or AZERO ONCE, the multimeter takes the autozero measurement
            when the first trigger arm event occurs for all events except TARM EXT which
            causes an autozero measurement when the TARM EXT command is executed.
            The autozero measurement will be updated whenever the measurement
            function, range, or integration time is changed (this update will be made when
            the trigger arm event occurs or TARM EXT is executed).\n
            -The display annunciator AZERO OFF illuminates when autozero is disabled.\n
            -Autozero cannot be disabled for DC current measurements.\n
            -For 2-wire ohms measurements with offset compensation enabled, the zero
            measurement and offset measurement are done simultaneously.\n
            -Autozero should be on for 4-wire ohms measurements. If you must disable
            autozero, be sure to make all measurement connections before disabling
            autozero and ensure that the lead resistance will not change. If you disable
            autozero before making the 4-wire connections, or if you have a varying lead
            resistance with autozero disabled (such as when scanning), you will get
            inaccurate 4-wire ohms measurements.\n

        Returns:
            bool: status
        """

        if state == 'ON' or state == 'OFF' or state == 'ONCE':
            return self.__write_data(f'AZERO {state}')
        else:
            return False
        
    def get_autozero(self) -> str:
        """Returns the current autozero setting.

        Returns:
            str: ON, OFF or ONCE
        """
        return self.__get_data(f'AZERO?')
    
    def set_fixedz(self, state = 'OFF') -> bool:
        """The FIXEDZ command enables or disables the fixed input resistance function for
        DC voltage measurements. When enabled, the multimeter maintains its input
        resistance at 10 megohms for all ranges. This prevents a change in input
        resistance (caused by a range change) from affecting the DC voltage
        measurements.

        Args:
            state (str, optional): ON (Fixed Z enabled) and OFF (FIXEDZ disabled).
            Remarks:
            - FIXEDZ remains enabled when you change from DC voltage measurements to
            2-wire or 4-wire ohms measurements. Resistance measurements made with
            FIXEDZ enabled will be in error because the multimeter's input resistance
            represents a 10 MOhm resistance in parallel with the input terminals.\n
            - FIXEDZ is temporarily disabled when you change from DC voltage
            measurements to AC voltage, AC+DC voltage, any type of current, frequency,
            or period measurements. For example, if FIXEDZ is enabled and you change
            from DC voltage measurements to AC voltage measurements, FIXEDZ
            becomes disabled. When you return to DC voltage measurements, however,
            FIXEDZ is once again enabled.\n

        Returns:
            bool: status

        """
        if state == 'ON' or state == 'OFF':
            return self.__write_data(f'FIXEDZ {state}')
        else:
            return False


    def get_fixedz(self) -> str:
        """Returns the current fixed input resistance setting.

        Returns:
            str: ON or OFF
        """
        return self.__get_data(f'FIXEDZ?')

    def get_integer_scale(self) -> str:
        """Returns the scale factor for readings output in the SINT or DINT formats.

        Remarks:
            -The scale factor is always 1 for the ASCII, SREAL, and DREAL output formats.\n
            -Readings output in the SINT or DINT formats (see the OFORMAT command)
            are first compressed by the multimeter so they may be expressed as integers.
            Multiplying the readings by the value returned by ISCALE? will restore them to
            their actual values. The scale factor is determined by the configuration of the
            multimeter when ISCALE? is executed. This includes the measurement
            function, range, and integration time. Therefore, the multimeter's
            configuration must be the same when the scale factor is retrieved as it was
            when the readings were taken. You can retrieve the scale factor after the
            multimeter is configured but before readings are triggered or immediately after
            the readings made.\n
            -You should not use the SINT or DINT output or memory format for frequency or
            period measurements when a real-time or post-process math function is
            enabled (except STAT or PFAIL) or when autorange is enabled.

        Returns:
            str: SINT, DINT and 1 for ASCII, SREAL, DREAL
        """
        return self.__get_data(f'ISCALE?')
    
    def set_level_triggering_voltage(self, percentage = 0, coupling = 'AC'):
        """The LEVEL command specifies the level triggering voltage (as a percentage of the
        present range) and the coupling (AC or DC) for level triggering. A level trigger
        event occurs when the input signal reaches the specified voltage on its
        positive-going or negative-going slope as specified by the SLOPE command.

        Args:
            percentage (int, optional): Specifies the percentage of the present range for level triggering. The valid range
            for this parameter is -500% to +500% in 5% steps for direct- or sub-sampling or
            -120% to 120% in 1% steps for DC voltage. The full scale values for direct-sampling are 500% (5 times) the ranges of 10 mV
            100 mV, 1 V, 10 V, and 100 V. When specifying the level triggering percentage,
            remember to use a percentage of the range. For example, assume the input signal
            has a peak value of 20 V and you are using the 10 V range. If you want to level
            trigger at 15 V, you would specify a level triggering percentage of 150% (LEVEL
            150 command). Defaults to 0.
            coupling (str, optional): The coupling parameter selects the coupling of the signal to the level-detection
            circuitry only. This does not affect the coupling of the signal being measured. Coupling should be 'DC' or 'AC'. Defaults to 'AC'.

        Remarks:
            -Level triggering can be used for DC voltage, direct-sampling, and
            sub-sampling. (The LEVEL command also affects the zero crossing threshold
            and the input signal coupling for frequency and period measurements.) For DC
            voltage and direct-sampling, level triggering can be used as the trigger event
            (TRIG LEVEL command) or the sample event (NRDGS n, LEVEL command). For
            sub-sampling, level triggering can be used for the sync source event only
            (SSRC LEVEL command).\n
            -Because of hysteresis, the actual level triggering point is the specified
            percentage ±4% of the measurement range.\n
            -Autozero should be disabled when using level triggering (AZERO OFF
            command) for DC voltage measurements. (Autozero doesn't apply to direct- or
            sub-sampling.)\n
            
        Returns:
            bool: status
        """

        if coupling == 'AC' or coupling == 'DC' and percentage >= -500 and percentage <= 500:
            return self.__write_data(f'LEVEL {percentage},{coupling}')
        else:
            return False
        
    def get_level_triggering_voltage(self) -> str:
        """Returns the level triggering voltage and coupling setting.

        Returns:
            str: level triggering voltage and coupling setting.
        """
        return self.__get_data(f'LEVEL?')
    
    def set_level_filter(self, state = 'ON') -> bool:
        """Level filter. Enables or disables the level filter function. When enabled, the level
        filter function connects a single pole low-pass filter circuit to the input of the
        level-detection circuitry. The low-pass filter has a 3-dB point of 75 kHz and
        prevents high frequency components from causing false triggers.

        Args:
            state (str, optional): ON (Level filter enabled) and OFF (Level filter disabled). Defaults to 'ON'.

        Remarks:
            - Level filtering can be used when level triggering for DC voltage, direct- and
            sub-sampling. The level filter can also be used to reduce sensitivity to noise for
            frequency and period measurements or when making AC or AC+DC voltage
            measurements using the synchronous method (SETACV SYNC command).\n

        Returns:
            bool: status
        """
        if state == 'ON' or state == 'OFF':
            return self.__write_data(f'LFILTER {state}')
        else:
            return False
        
    def get_level_filter(self) -> str:
        """Returns the current level filter setting.

        Returns:
            str: ON or OFF
        """
        return self.__get_data(f'LFILTER?')
    
    def set_adc_reference_frequency(self, freq = 50) -> bool:
        """The LFREQ command allows you to specify the A/D converter's reference
        frequency or measure the line frequency and set the reference frequency to the
        measured value.

        Args:
            freq (int, str, optional): Allows you to specify the reference frequency. The valid range for the frequency
            parameter is 45 - 65 Hz, or 360 - 440 Hz. When you specify a frequency in the
            range of 360 - 440 Hz, the multimeter divides that value by 8. For example, if you
            specify LFREQ 400, the multimeter sets the reference frequency to 400/8 = 50 Hz. Defaults to 50.
            LINE Measures the exact value of the line frequency and sets the reference frequency to
            that value (or measured value/8 if the measured value is between 360 and
            440 Hz).

        Remarks:
            -When power is applied, the multimeter measures the line frequency, rounds it
            to 50 or 60 Hz, and sets the A/D Converter's reference frequency to the
            rounded value. (For a 400 Hz power line frequency, the multimeter uses 50 Hz
            as a reference frequency which is a subharmonic of 400 Hz.)\n
            - The step size for the period of the reference frequency is 100 ns. For example,
            the period of a 60 Hz reference frequency is 1/60 Hz = .0166666... Since the
            step size is 100 ns, the multimeter uses the value of .0166667 s. The step size
            is most noticeable when using the LFREQ? query command. For example, if
            you have specified 60 Hz as the reference frequency, the LFREQ? returns
            59.99988 (1/.0166667).\n
            - The multimeter multiplies the period of the reference frequency times the
            specified number of power line cycles (NPLC command) to determine the
            actual integration time. The multimeter's normal mode noise rejection (NMR)
            specifications for DC and resistance measurements are related to the accuracy
            of the A/D converter's reference frequency.\n

        Returns:
            bool: status
        """
        if (freq >= 50 and freq <= 65) or (freq >= 360 and freq <= 440) or freq == 'LINE':
            return self.__write_data(f'LFREQ {freq}')
        else:
            return False
        
    def get_adc_reference_frequency(self) -> str:
        """Returns the A/D converter's reference frequency.

        Returns:
            str: reference frequency.
        """
        return self.__get_data(f'LFREQ?')
    

    def set_realtime_math(self, operation_a, operation_b=None) -> bool:
        """The MATH command enables or disables real-time math operations.

        Args:
            operation_a and operation_b (str): Specifies the real-time math operation.
            The multimeter can perform the following real-time math functions: 
            -OFF (0)- Disables all enabled real-time math operations \n
            -CONT (1)- Enables the previous math operation. To resume two math operations, send MATH CONT,CONT \n
            -CTHRM (2)- Result = temperature (Celsius) of a 5 kW thermistor (40653B). Function must be OHM or OHMF (10 kW range or higher). \n
            -DB (3)- Result = 20 x Log10(reading/REF register). The REF register is initialized to 1, yielding dBV. \n
            -DBM (4)- Result =10 x log10(reading2/RES register/1 mW). Function must be ACV, DCV, or ACDCV. \n
            -FILTER (5)- Result = output of exponentially weighted digital low-pass filter. Response is set by DEGREE register. \n
            -FTHRM (6)- Result = temperature (Fahrenheit) of a 5 kW thermistor (40653B). Function must be OHM or OHMF (10 kW range or higher). \n
            -NULL (7)- Result = reading-OFFSET register. The OFFSET register is set to first reading—after that you can change it. \n
            -PERC (8)- Result = ((reading - PERC register) / PERC register x 100.\n
            -PFAIL (9)- Reading vs. MAX and MIN registers. \n
            -RMS (10)- Result = squares reading, applies FILTER operation, takes square root. \n
            -SCALE (11)- Result = (reading-OFFSET register) / SCALE register. \n
            -STAT (12)- Performs statistical calculations on the present set of readings and
                stores results in these registers:
                SDEV = standard deviation
                MEAN = average of readings
                NSAMP = number of readings
                UPPER = largest reading
                LOWER = smallest reading \n
            -CHTRM2K (13)- Result = temperature (Celsius) of a 2 kOhm thermistor (40653A). Function must be OHM or OHMF. \n
            -CHTRM10K (14)- Result = temperature (Celsius) of a 10 kOhm thermistor (40653C). Function must be OHM or OHMF.\n
            -FTHRM2K (15)- Result = temperature (Fahrenheit) of a 2 kOhm thermistor (40653A). Function must be OHM or OHMF.\n
            -FTHRM10K (16)- Result = temperature (Fahrenheit) of a 10 kOhm thermistor (40653C). Function must be OHM or OHMF. \n
            -CRTD85 (17)- Result = temperature (Celsius) of 100 Ohm RTD with alpha of 0.00385 (40654A or 406548). Function must be OHM or OHMF. \n
            -CRTD92 (18)- Result = temperature (Celsius) of 100 Ohm RTD with alpha of 0.003916. Function must be OHM or OHMF. \n
            -FRTD85 (19)- Result = temperature (Fahrenheit) of 100 Ohm RTD with alpha of 0.00385 (40654A or 406548). Function must be OHM or OHMF. \n
            -FRTD92 (20)- Result = temperature (Fahrenheit) of 100 Ohm RTD with alpha of 0.003916. Function must be OHM or OHMF. \n
        
        Remarks:
            - The FILTER, RMS, STAT, or PFAIL math operations are performed on all
            subsequent readings. However, whenever the multimeter's configuration is
            changed, the previous math results are erased and the operation starts over on
            the new readings. All other math operations stay enabled until you set MATH
            OFF, execute the MATH command specifying other math operation(s), or
            enable post-process math operation(s) (except MMATH PFAIL or MMATH STAT
            as described under the MMATH command).\n
            -When two real-time math operations are enabled, operation_a is performed on
            the reading first. Next, operation_b is performed on the result of the first
            operation.
            -When a real-time math operation is enabled, the display's half digit becomes a
            full digit. For example, if you are making 4.5 digit AC voltage measurements
            and then enable the SCALE math operation, the display is capable of showing
            5 full digits.
            -Math registers may be written to with the SMATH command. Math registers
            may be read with the RMATH command.

        Returns:
            bool: status
        """
        if operation_a == 'OFF':
            return self.__write_data(f'MATH {operation_a}')
        elif operation_a in ['CONT', 'CTHRM', 'DB', 'DBM', 'FILTER', 'FTHRM', 'NULL', 'PERC', 'PFAIL', 'RMS', 'SCALE', 'STAT', 'CHTRM2K', 'CHTRM10K', 'FTHRM2K', 'FTHRM10K', 'CRTD85', 'CRTD92', 'FRTD85', 'FRTD92'] and operation_b in ['OFF', 'CONT', 'CTHRM', 'DB', 'DBM', 'FILTER', 'FTHRM', 'NULL', 'PERC', 'PFAIL', 'RMS', 'SCALE', 'STAT', 'CHTRM2K', 'CHTRM10K', 'FTHRM2K', 'FTHRM10K', 'CRTD85', 'CRTD92', 'FRTD85', 'FRTD92']:
            return self.__write_data(f'MATH {operation_a},{operation_b}')
        else:
            return False
        
    def get_realtime_math(self) -> str:
        """Returns the current real-time math operation.

        Returns:
            str: real-time math operation.
        """
        return self.__get_data(f'MATH?')
    
    def set_postprocess_math(self, operation_a, operation_b) -> str:
        """"Enables or disables post-process math operations.

        Args:
            operation_a and operation_b (str): Specifies the real-time math operation.
            The multimeter can perform the following real-time math functions: 
            -OFF (0) - Disables all enabled real-time math operations \n
            -CONT (1)- Enables the previous math operation. To resume two math operations, send MATH CONT,CONT \n
            -CTHRM (2)- Result = temperature (Celsius) of a 5 kW thermistor (40653B). Function must be OHM or OHMF (10 kW range or higher). \n
            -DB (3)- Result = 20 x Log10(reading/REF register). The REF register is initialized to 1, yielding dBV. \n
            -DBM (4)- Result =10 x log10(reading2/RES register/1 mW). Function must be ACV, DCV, or ACDCV. \n
            -FILTER (5)- Result = output of exponentially weighted digital low-pass filter. Response is set by DEGREE register. \n
            -FTHRM (6)- Result = temperature (Fahrenheit) of a 5 kW thermistor (40653B). Function must be OHM or OHMF (10 kW range or higher). \n
            -NULL (7)- Result = reading-OFFSET register. The OFFSET register is set to first reading—after that you can change it. \n
            -PERC (8)- Result = ((reading - PERC register) / PERC register x 100.\n
            -PFAIL (9)- Reading vs. MAX and MIN registers. \n
            -RMS (10)- Result = squares reading, applies FILTER operation, takes square root. \n
            -SCALE (11)- Result = (reading-OFFSET register) / SCALE register. \n
            -STAT (12)- Performs statistical calculations on the present set of readings and
                stores results in these registers:
                SDEV = standard deviation
                MEAN = average of readings
                NSAMP = number of readings
                UPPER = largest reading
                LOWER = smallest reading \n
            -CHTRM2K (13)- Result = temperature (Celsius) of a 2 kOhm thermistor (40653A). Function must be OHM or OHMF. \n
            -CHTRM10K (14)- Result = temperature (Celsius) of a 10 kOhm thermistor (40653C). Function must be OHM or OHMF.\n
            -FTHRM2K (15)- Result = temperature (Fahrenheit) of a 2 kOhm thermistor (40653A). Function must be OHM or OHMF.\n
            -FTHRM10K (16)- Result = temperature (Fahrenheit) of a 10 kOhm thermistor (40653C). Function must be OHM or OHMF. \n
            -CRTD85 (17)- Result = temperature (Celsius) of 100 Ohm RTD with alpha of 0.00385 (40654A or 406548). Function must be OHM or OHMF. \n
            -CRTD92 (18)- Result = temperature (Celsius) of 100 Ohm RTD with alpha of 0.003916. Function must be OHM or OHMF. \n
            -FRTD85 (19)- Result = temperature (Fahrenheit) of 100 Ohm RTD with alpha of 0.00385 (40654A or 406548). Function must be OHM or OHMF. \n
            -FRTD92 (20)- Result = temperature (Fahrenheit) of 100 Ohm RTD with alpha of 0.003916. Function must be OHM or OHMF. \n
        
        Remarks:
            - Any enabled post-process math operations except STAT and PFAIL are
            performed on each reading as it is removed or copied from reading memory to
            the display or the GPIB output buffer. (The readings in memory are not altered
            by any post-process math operation.) The STAT or PFAIL post-process math
            operations are performed using the readings in memory immediately after
            executing the MMATH command. (The STAT and PFAIL operations are not
            updated for any additional readings placed in memory after executing the
            MMATH command.)\n
            -For the STAT operation, results are stored in the SDEV, MEAN, NSAMP,UPPER,
            and LOWER math registers (refer to the RMATH command for information on
            these registers).\n
            -For the PFAIL operation, whenever an out of limit reading is detected, bit
            number 1 in the status register is set (this sets the GPIB SRQ fine if enabled by
            the RQS command) and the display shows the FAILED LOW or FAILED HIGH
            message.\n
            -An enabled post-process math operation remains enabled until you set
            MMATH OFF, enable a real-time math operation (MATH command), or execute
            the MMATH command specifying another math operation (except as described
            in the following remark).\n
            - When MMATH is executed from the front panel, the result goes to the display
            only. When MMATH is executed from remote, the result goes to the output
            buffer only.\n
            - When two post-process math operations are enabled, operation_a is
            performed on the reading first. Next, operation_b is performed on the result of
            the first operation.\n
            - When a post-process math operation is enabled, the display's half digit
            becomes a full digit. For example, if you are making 4.5 digit AC voltage
            measurements and then enable the SCALE operation, the display is capable of
            showing 5 full digits.\n
            - Math registers may be written to with the SMATH command. Math registers
            may be read with the RMATH command.\n

        Returns:
            bool: status
        """

        if operation_a in ['OFF', 'CONT', 'CTHRM', 'DB', 'DBM', 'FILTER', 'FTHRM', 'NULL', 'PERC', 'PFAIL', 'RMS', 'SCALE', 'STAT', 'CHTRM2K', 'CHTRM10K', 'FTHRM2K', 'FTHRM10K', 'CRTD85', 'CRTD92', 'FRTD85', 'FRTD92'] and operation_b in ['OFF', 'CONT', 'CTHRM', 'DB', 'DBM', 'FILTER', 'FTHRM', 'NULL', 'PERC', 'PFAIL', 'RMS', 'SCALE', 'STAT', 'CHTRM2K', 'CHTRM10K', 'FTHRM2K', 'FTHRM10K', 'CRTD85', 'CRTD92', 'FRTD85', 'FRTD92']:
            return self.__write_data(f'MMATH {operation_a},{operation_b}')
        else:
            return False
        
    def get_postprocess_math(self) -> str:
        """Clears reading memory and designates the storage format for new readings.

        Returns:
            str: post-process math operation.
        """
        return self.__get_data(f'MMATH?')
    
    def set_memory_format(self, format) -> str:
        """The OFORMAT command specifies the format for the readings stored in memory.

        Args:
            format (str): Specifies the format for the readings stored in memory. The multimeter can store
            readings in the following formats:\n
            -ASCII (1) - ASCII characters\n
            -SINT (2) - 16-bit signed integer\n
            -DINT (3)- 32-bit signed integer\n
            -SREAL (4)- 32-bit floating point\n
            -DREAL (5)- 64-bit floating point\n

        Remarks:
            - The multimeter indicates an overload by storing the value ±1E+38 in memory
            instead of the reading. When overload values are recalled to the display, the
            value ±1E+38 is displayed. When overload values are transferred from reading
            memory to the GPIB output buffer, they are converted to the overload number
            for the specified output format.\n
            - When using the SINT or DINT memory format, the multimeter stores each
            reading assuming a certain scale factor. This scale factor is based on the
            present measurement function, range, A/D setting, and enabled math
            operations. When you recall a reading, the multimeter calculates the scale
            factor based on the present measurement function, range, A/D setting, and
            enabled math operations. It then multiplies the scale factor by the stored
            reading and sends the result (recalled reading) to the display or the output
            buffer. Therefore, always ensure that the multimeter's configuration is the
            same when storing and recalling data in the SINT or DINT format.\n
            - You should not use the SINT or DINT output or memory format for frequency or
            period measurements when a real-time or post-process math function is
            enabled (except STAT or PFAIL) or when autorange is enabled.\n
            - The memory format does not affect the output format specified by the
            OFORMAT command.\n
            - You enable reading memory using the MEM command. You access stored
            readings using the RMEM command or by using the "implied read."\n
            -When using reading memory for sub-sampled measurements (SSAC or SSDC
            command), the memory format must be set to SINT, the memory mode must
            be FIFO (MEM FIFO command), and reading memory must be empty (done by
            executing the MEM FIFO command) before samples are taken. If these
            requirements are not met when the trigger arm event occurs, an error is
            generated.\n

        Returns:
            bool: status
        """
        if format in ['ASCII', 'SINT', 'DINT', 'SREAL', 'DREAL']:
            return self.__write_data(f'MFORMAT {format}')
        else:
            return False
        
    def get_memory_format(self) -> str:
        """Returns the format for the readings stored in memory.

        Returns:
            str: memory format.
        """
        return self.__get_data(f'MFORMAT?')
    
    def set_nplc(self, nplc=0) -> str:
        """Specifies the A/D converter's integration time in
            terms of power line cycles. Integration time is the time during which the A/D
            converter measures the input signal.

        Args:
            nplc (int, optional): The primary use of the NPLC command is to establish normal mode noise
            rejection (NMR) at the A/D converter's reference frequency (LFREQ command).
            Any value ≥1 for the power_line_cycles parameter provides at least 60 dB of NMR
            at the power line frequency. Any value <1 provides no NMR; it only sets the
            integration time for the A/D converter. The ranges and the incremental step sizes
            for the power_line_cycles parameter are: 0 - 1 PLC in .000005 PLC steps for 50 Hz reference frequency,
            1 - 10 PLC in 1 PLC steps, 10 - 1000 PLC in 10 PLC steps.

        Remarks:
            - For the ACV and ACDCV (SETACV ANA method only), ACT, ACDCI, DCI, DCV,
            OHM, and OHMF measurement functions, resolution is determined by the A/D
            converter's integration time. The integration time has no effect on FREQ or
            PER. For sampled ACV or ACDCV (SETACV SYNC or SETACV RNDM), the
            integration time is selected automatically and the specified resolution is
            achieved by varying the number of samples taken. For direct- or sub-sampled
            digitizing, the integration time is fixed and cannot be changed.\n
            - Since the NPLC and APER commands both set the integration time, executing
            either will cancel the integration time previously established by the other. The
            RES command or the %_resolution parameter of a function command or the
            RANGE command can also be used to indirectly select an integration time. An 
            interaction occurs between NPLC (or APER) when you specify resolution as follows:
            * If you send the NPLC (or APER) command before specifying resolution, the
            multimeter satisfies the command that specifies greater resolution (more
            integration time).\n
            * If you send the NPLC (or APER) command after specifying resolution, the
            multimeter uses the integration time specified by the NPLC (or APER)
            command, and any previously specified resolution is ignored.\n
            * The more common approach is the first of the two shown above; i.e., the NPLC
            command is executed first to establish normal mode noise rejection (NMR),
            then %_resolution is specified with a function or RANGE command. This
            ensures you will have NMR and at least the required resolution.\n

        Returns:
            bool: status
        """
        
        if nplc >= 0 and nplc <= 1000:
            return self.__write_data(f'NPLC {nplc}')
        else:
            return False
        

    def get_nplc(self) -> str:
        """Returns the A/D converter's integration time in terms of power line cycles.

        Returns:
            str: power line cycles.
        """
        return self.__get_data(f'NPLC?')
    
    def set_resistance_offset_compensation(self, state = 'ON') -> bool:
        """The OCOMP command enables or disables the offset compensated ohms
            function.

        Args:
            state (str, optional): ON (Offset compensation enabled) and OFF (Offset compensation disabled). Defaults to 'ON'.

        Remarks:
            - With offset compensation enabled, the multimeter measures the external
            offset voltage (with the ohms current source shut off) before each resistance
            reading and subtracts the offset from the following reading. This prevents the
            offset voltage from affecting the resistance reading, but it doubles the time
            required per reading.\n
            - You can use offset compensated ohms on both 2-wire and 4-wire resistance
            measurements. When you have offset compensation enabled and change from
            ohms to some other measurement function (DCV, ACV, etc.), offset
            compensation is temporarily disabled. When you return to 2-wire or 4-wire
            ohms, however, offset compensation is once again enabled.\n
            - The multimeter can only perform offset compensation on the 10 Ohm through
            100 kOhm ranges. If OCOMP is enabled when using the 1 MOhm through 1 GOhm
            ranges, readings are made without offset compensation.\n

        Returns:
            bool: status
        """
        if state == 'ON' or state == 'OFF':
            return self.__write_data(f'OCOMP {state}')
        else:
            return False

    def get_resistance_offset_compensation(self) -> str:
        """Returns the current offset compensated ohms setting.

        Returns:
            str: ON or OFF
        """
        return self.__get_data(f'OCOMP?')
    
    def set_output_format(self, format) -> str:
        """Designates the GPIB output format for readings sent directly to 
        the controller or transferred from reading memory to the controller.

        Args:
            format (str): Specifies the format for the readings output to the GPIB interface. The multimeter
            can output readings in the following formats:\n
            -ASCII (1) - ASCII characters\n
            -SINT (2) - 16-bit signed integer\n
            -DINT (3)- 32-bit signed integer\n
            -SREAL (4)- 32-bit floating point\n
            -DREAL (5)- 64-bit floating point\n

        Remarks:
            - The ASCII output format sends the cr lf (carriage return, line feed) to indicate
            the end of the transmission to most computers. The SINT, DINT, SREAL, and
            DREAL output formats, however, do not send cr lf. With any format, you can
            use the END command to indicate the end of the transmission using the GPIB
            EOI function. Refer to the END command for more information.\n
            - When using the ASCII format, 2 additional bytes are required for the
            carriage-return, line-feed (cr,lf) end of line sequence. The cr,lf is used only for
            the ASCII format and normally follows each reading output in ASCII format.
            However, when using the ASCII output format and multiple readings are
            recalled from reading memory using the RMEM command, the multimeter
            places a comma between readings (comma = 1 byte). In this case, the cr,lf
            occurs only once, following the last reading in the group being recalled.
            Commas are not used when readings are output directly to the bus (reading
            memory disabled), when readings are recalled using "implied read," or when
            using any other output format.\n
            - The multimeter indicates an overload condition (input greater than the present
            range can measure) by outputting the largest number possible for the
            particular output format as follows:
            SINT format: +32767 or -32768 (unscaled)
            DINT format: +2.147483647E+9 or -2.147483648E+9 (unscaled)
            ASCII, SREAL, DREAL: +/-1.0E+38\n
            - When reading memory is disabled, executing the SSAC or SSDC command
            (sub-sampling) automatically sets the output format to SINT regardless of the
            previously specified format. You must use the SINT output format when
            sub-sampling and not using reading memory.\n
            - The output format applies only to readings transferred over the GPIB bus.
            Responses to query commands are always output in ASCII format regardless of
            the specified output format. Following the query response, the output format
            returns to the specified type. The output format does not affect the memory
            format specified by the MFORMAT command.\n
            - When using the SINT or DINT output formats, the multimeter applies a scale
            factor to each reading. This scale factor is based on the present measurement
            function, range, A/D setting, and enabled math operations. Therefore, ensure
            that the multimeter's configuration is the same when retrieving the scale
            factor (ISCALE? command) as it was when the readings were made.\n
            - You should not use the SINT or DINT output or memory format for frequency or
            period measurements when a real-time or post-process math function is
            enabled (except STAT or PFAIL) or when autorange is enabled.


        Returns:
            bool: status
        """
        if format in ['ASCII', 'SINT', 'DINT', 'SREAL', 'DREAL']:
            return self.__write_data(f'OFORMAT {format}')
        else:
            return False
        

    def get_output_format(self) -> str:
        """Returns the GPIB output format for readings sent directly to the controller or transferred from reading memory to the controller.

        Returns:
            str: output format.
        """
        return self.__get_data(f'OFORMAT?')
    
    def set_ratio_enabled(self, state = 'ON') -> bool:
        """The RATIO command instructs the multimeter to measure a DC reference voltage
            applied to the Ohm Sense terminals and a signal voltage applied to the Input
            terminals. The multimeter then computes the ratio as: Ratio = Signal Voltage / DC Reference Voltage.

        Args:
            state (str, optional): ON (Enables ratio measurements using the present measurement
            function (DCV, ACV, or ACDCV)) and OFF (Disables ratio measurements). Defaults to 'ON'.
        
        Remarks:
            - The Ohm Sense LO and the Input LO terminals must have a common reference
            and cannot have a voltage difference >0.25 V.\n
            - The signal voltage can be measured using the DCV, ACV, or ACDCV
            measurement function. (For ACV or ACDCV, any of the three measurement
            methods ANA, RNDM, or SYNC may be used.) The multimeter always uses
            DCV for the reference voltage measurement. The measurable reference 
            voltage range is ±12 VDC (autorange only). To specify ratio measurements,
            you first select the measurement function (and the measurement method for
            ACV or ACDCV) and then enable ratio measurements with the RATIO
            command (see example below).\n

        Returns:
            bool: status
        """
        if state == 'ON' or state == 'OFF':
            return self.__write_data(f'RATIO {state}')
        else:
            return False
        
    def get_ratio_enabled(self) -> str:
        """Returns the ratio measurement setting.

        Returns:
            str: ON or OFF
        """
        return self.__get_data(f'RATIO?')
    
    def set_voltage_ac_conversion_technique(self, technique = 'ANA') -> bool:
        """The SETACV command specifies the method used to measure AC voltage.

        Args:
            technique (str, optional): Specifies the method used to measure AC voltage. The multimeter can measure
            AC voltage using the following methods:\n
            -ANA (1) - Analog RMS conversion.\n
            -RNDM (2) - Random sampling conversion.\n
            -SYNC (3) - Synchronous sampling conversion.\n

        Remarks:
            - Bandwidth limitations vary with the conversion technique selected.

        Returns:
            bool: status
        """
        if technique in ['ANA', 'RNDM', 'SYNC']:
            return self.__write_data(f'SETACV {technique}')
        else:
            return False
        
    def get_voltage_ac_conversion_technique(self) -> str:
        """Returns the method used to measure AC voltage.

        Returns:
            str: method used to measure AC voltage.
        """
        return self.__get_data(f'SETACV?')
    
    def set_trigger_signal_slope(self, slope='POS'):
        """SLOPE is used in conjunction with the LEVEL command and specifies which slope
        of the signal will be used by the level-detection circuitry.

        Args:
            slope (str, optional): Specifies the slope of the signal that triggers a level trigger event. The slope
            can be positive-going slop (POS (1)) or negative-going slope (NEG (0)). Defaults to 'POS'.

        Returns:
            bool: status
        """
        if slope == 'POS' or slope == 'NEG':
            return self.__write_data(f'SLOPE {slope}')
        else:
            return False
        
    def get_trigger_signal_slope(self) -> str:
        """Returns the slope of the signal that triggers a level trigger event.

        Returns:
            str: slope of the signal.
        """
        return self.__get_data(f'SLOPE?')
    
    def get_subsampling_parameters(self) -> str:
        """Sub-sampling parameters query. Returns the parameters necessary to
            reconstruct a sub-sampled waveform (SSAC or SSDC command) when the
            samples are sent directly to the GPIB output buffer. (Reconstruction is automatic
            when the samples are sent directly to reading memory.)\n
            The first parameter returned by SSPARM? is the number of bursts that contained
            N samples. The second parameter is the number of bursts that contained N-1
            samples. The third parameter returned is the value of N. For example, assume you
            are sub-sampling a 10 kHz signal and specify 22 samples with an
            effective_interval of 5 μs. In this example, the multimeter must use a total of 4
            bursts: 2 bursts contain 6 samples each and 2 bursts contain 5 samples each. The
            values returned by SSPARM? are then 2, 2, and 6.

        Returns:
            str: sub-sampling parameters.
        """
        return self.__get_data(f'SSPARM?')
    
    def set_subsampling_sync_source(self, source = 'LEVEL', mode = 'AUTO') -> bool:
        """Sync source. For sub-sampling (SSAC or SSDC command), the SSRC command
            allows you to synchronize bursts to an external signal or to a voltage level on the
            input signal.
            For synchronous ACV or ACDCV (SETACV SYNC command), the SSRC command
            allows you to synchronize sampling to an external signal. You can also use the
            HOLD parameter to prevent the measurement method from changing to random
            should level triggering not occur within certain time limits. The time limits are
            determined by the AC bandwidth (ACBAND command) setting.

        Args:
            source (str, optional): Specifies the source of the trigger signal for sub-sampling. The multimeter can
            use the following sources for the trigger signal:\n
            -EXT (2) - Synchronize to external input on the rear panel Ext Trig connector.\n
            -LEVEL (7) - Synchronize to a voltage Level (LEVEL command) on the input
            signal using the slope specified by the SLOPE command. For synchronous ACV or ACDCV, the level triggering voltage 
            (LEVEL command) and the slope (SLOPE command) are determined automatically and cannot be specified.\n
            mode (str, optional): The mode parameter applies only to synchronous ACV or ACDCV. The choices are:\n
                -AUTO (1) -For synchronous AC or ACDCV (SETACV SYNC) using level
                triggering (default mode), if the input signal is removed during a
                reading and does not return within a certain amount of time, the
                measurement method changes to random so that the reading can
                be completed. (After the reading, the measurement method
                returns to SYNC.)\n
                -HOLD (4) - The measurement method will not automatically change from
                synchronous to random when the input signal is removed.

        Remarks:
            - For sub-sampling, the trigger event and the sample event are ignored. The
            only triggering events that apply to sub-sampling are the trigger arm event
            (TARM command) and the sync source event (SSRC command). For
            synchronous ACV or ACDCV measurements (SETACV SYNC command), the
            specified trigger arm event (TARM command), trigger event (TRIG command),
            and sample event (NRDGS command) must all be satisfied before the sync
            source event can initiate sampling.\n
            -For sub-sampling and synchronous AC measurements, bursts of samples are
            taken on more than one period of the waveform. The sync source event
            synchronizes these bursts to the periods of the input signal (that is, a sync
            source event should typically occur once for each period).\n

        Returns:
            bool: status
        """
        if source in ['EXT', 'LEVEL'] and mode in ['AUTO', 'HOLD']:
            return self.__write_data(f'SSRC {source},{mode}')
        else:
            return False
        
    def get_subsampling_sync_source(self) -> str:
        """Returns the source of the trigger signal for sub-sampling.

        Returns:
            str: source of the trigger signal.
        """
        return self.__get_data(f'SSRC?')
    
    def set_effective_interval_between_samples(self, effective_interval=20E-6, num_samples=1024) -> bool:
        """The SWEEP command specifies the effective_interval between samples (readings
        and the total number of samples taken per trigger event [most measurement
        functions] or per trigger arm event (sub-sampling only).

        Args:
            effective_interval (int): For sub-sampling (SSAC or SSDC), this parameter specifies the spacing of
            samples in the reconstructed waveform (see Chapter 5 for details). For all other
            measurement functions, this parameter specifies the actual time interval from one
            sample to the next. For sub-sampling, the valid range of this parameter is 10E-9
            to 6000 seconds with 10 ns increments; for all other measurement functions the
            range is (1/maximum reading rate) to 6000 seconds in 100 ns increments.\n
            num_samples (int): Specifies the number of samples to be taken. The valid range for this parameter is
            1 to 1.67E+7.\n

        Remarks:
            - The minimum effective interval for DC voltage measurements is 10 μs; for
            direct-sampling, 20 μs; for sub-sampling, 10 nanoseconds.\n
            - The SWEEP command can be used to replace the NRDGS n,TIMER command
            and the TIMER command. The SWEEP and NRDGS are interchangeable; the
            multimeter uses whichever command was executed last in the programming.
            Executing the SWEEP command automatically sets the sample event to
            TIMER. In the power-on, RESET, or PRESET state, the multimeter uses the
            NRDGS command. The power-on values for SWEEP can only be used for
            sub-sampling (since NRDGS does not apply to sub-sampling).\n
            - You cannot use the SWEEP or TIMER functions for AC or AC+DC voltage
            measurements using the synchronous or random methods (SETACV SYNC or
            RNDM) or for frequency or period measurements.\n
            - When using the SWEEP command (or TIMER event), autoranging is suspended
            (typically you should select a fixed range when using SWEEP).\n


        Returns:
            bool: status
        """ 

        if effective_interval >= 10E-9 and effective_interval <= 6000 and num_samples >= 1 and num_samples <= 1.67E+7:
            return self.__write_data(f'SWEEP {effective_interval},{num_samples}')
        else:
            return False
        
    def get_effective_interval_between_samples(self) -> str:
        """Returns the effective_interval between samples.

        Returns:
            str: effective_interval between samples.
        """
        return self.__get_data(f'SWEEP?')
    
    def set_timer_interval(self, interval=1) -> bool:
        """The TIMER command defines the time interval for the TIMER sample event in the
        NRDGS command. When using the TIMER event, the time interval is inserted
        between readings.

        Args:
            interval (int): The valid range of the time parameter is (1 /maximum sampling rate) to 6000
            seconds in 100 ns increments. Default is 1 second.

        Remarks:
            - When using the TIMER event, the first reading occurs without the time interval.
            However, you can insert a time interval before the first reading using the
            DELAY command.\n
            - When using the TIMER event, autoranging is suspended (typically you should
            select a fixed range when using the TIMER event). If autoranging was enabled
            when you specified the TIMER sample event, autoranging will resume when
            you specify another sample event.\n
            - The SWEEP command can be used to replace the two commands:
            NRDGSn,TIMER and TIMER n for any measurement function. The SWEEP and
            NRDGS are interchangeable; the multimeter uses whichever command was
            executed last in the programming. Executing the SWEEP command
            automatically sets the sample event to TIMER. In the power-on, RESET, or
            PRESET state, the multimeter uses the NRDGS command. The power-on
            values for SWEEP can only be used for sub-sampling (since NRDGS does not
            apply to sub-sampling).\n
            - You cannot use the TIMER (or SWEEP) event for AC or AC+DC voltage
            measurements using the synchronous or random methods (SETACV SYNC or
            RNDM) or for frequency or period measurements.\n

        Returns:
            bool: status
        """
        if interval > 0 and interval <= 6000:
            return self.__write_data(f'TIMER {interval}')
        else:
            return False
        
    def get_timer_interval(self) -> str:
        """Returns the time interval for the TIMER sample event.

        Returns:
            str: time interval.
        """
        return self.__get_data(f'TIMER?')
    
    def set_ac_band(self, low_frequency=20, high_frequency=20E6) -> bool:
        """Specifies the frequency content (bandwidth) of the input signal
        for all AC or AC+DC measurements. Specifying the bandwidth allows the
        multimeter to configure for the fastest possible measurements.

        Args:
        low_frequency (int): Specifies the lowest expected frequency component of the input signal. Default is 20 Hz.\n
        high_frequency (int): Specifies the highest expected frequency component of the input signal. Default is 20 MHz.\n

        Remarks:
            - For synchronous ACV or ACDCV (SETACV SYNC command), the bandwidth
            parameters are used by the multimeter to calculate time-out values and
            sampling parameters. When using level triggering (default mode), if the input
            signal is removed during a reading and does not return within the time limits,
            the measurement method changes to random so that the reading can be
            completed. (After the reading, the measurement method returns to SYNC.) For
            synchronous ACV or ACDCV, it is very important that the specified bandwidth
            corresponds to the frequency content of the signal being measured.\n
            - For frequency or period measurements with autorange enabled, the
            bandwidth parameters are used to determine the amount of time needed for
            autoranging. For these measurements, it is very important that the specified
            bandwidth (especially low_frequency) corresponds to the frequency content of
            the signal being measured.\n
            -If you are unsure of the frequency content of the input signal, default the
            ACBAND parameters.

        Returns:
            bool: status
        """

        if low_frequency > 0 and high_frequency > 0:
            return self.__write_data(f'ACBAND {low_frequency},{high_frequency}')
        else:
            return False
        
    def get_ac_band(self) -> str:
        """Returns the frequency content (bandwidth) of the input signal.

        Returns:
            str: frequency content (bandwidth) of the input signal.
        """
        return self.__get_data(f'ACBAND?')
    
    def set_frequency_source(self, source = 'VOLT') -> bool:
        """Frequency source. Specifies the type of signal to be used as the input signal for
        frequency or period measurements.

        Args:
            source (str, optional): The source parameter choices are:\n
            -ACV (2) - AC voltage (FREQ 1 Hz - 10 MHz; PER 100 ns - 1 s).\n
            -ACDCV (3) - AC+DC voltage (FREQ 1 Hz - 10 MHz; PER 100 ns - 1 s).\n
            -ACI (7) - AC current (FREQ 1 Hz - 100 kHz; PER 10 μs - 1 s).\n
            -ACDCI (8) - AC current (FREQ 1 Hz - 100 kHz; PER 10 μs - 1 s).\n
            
        Returns:
            bool: status
        """

        if source in ['VOLT', 'ACV', 'ACDCV', 'ACI', 'ACDCI']:
            return self.__write_data(f'FSOURCE {source}')
        else:
            return False
        
    def get_frequency_source(self) -> str:
        """Returns the type of signal to be used as the input signal for frequency or period measurements.

        Returns:
            str: type of signal.
        """
        return self.__get_data(f'FSOURCE?')
    
    def autocalibration(self, type = 'ALL', security_code = None) -> bool:
        """Autocal. Instructs the multimeter to perform one or all of its self calibrations.

        Args:
            type (str, optional): Specifies the type of calibration to be performed. The choices are:\n
            -ALL (0) - Performs the DCV, OHMS, and AC autocals.\n
            -DCV (1) - DC voltage gain and offset.\n
            -AC (2) - ACV flatness, gain, and offset.\n
            -OHMS (4) - OHMS gain and offset.\n
            security_code (str, int, optional): When autocal is secured, you must enter the correct security code to perform an
            autocal. When autocal is not secured, no security code is required. Refer to the
            SECURE command for more information on the security code and how to secure
            or unsecure autocal. Defaults to None.

        Remarks:
            - The AC autocal performs specific enhancements for ACV or ACDCV (all
            measurement methods), ACI or ACDCI, DSAC, DSDC, SSAC, SSDC, FREQ, and
            PER measurements.\n
            - The OHMS autocal performs specific enhancements for 2- or 4-wire ohms,
            DCI, and ACI measurements.\n
            - Always disconnect any AC input signals before you perform an autocal. If you
            leave an input signal connected to the multimeter, it may adversely affect the
            autocal.\n
            - The autocal constants are stored in continuous memory (they remain intact
            when power is removed). You do not necessarily need to perform autocal
            simply because power has been cycled.\n
            - The approximate time required to perform each autocal routine is:\n
            ALL: 16 minutes\n
            DCV: 2 minutes 45 seconds\n
            AC: 2 minutes 45 seconds\n
            OHMS: 11 minutes\n
            - After performing autocal, let the instrument sit for the recommended time
            shown below before taking a reading, to allow the relays to thermally stabilize:\n
            ACAL ALL 30 minutes\n
            ACAL DCV 15 minutes\n
            ACAL OHM 30 minutes\n
            ACAL ACV 15 minutes\n

        Returns:
            bool: status
        """

        if type in ['ALL', 'ADC', 'INPUT', 'SELF']:
            if security_code is None:
                return self.__write_data(f'ACAL {type}')
            else:
                return self.__write_data(f'ACAL {type},{security_code}')
        else:
            return False
        
    def get_auxiliary_error(self) -> str:
        """Auxiliary error. When a hardware error is detected. the multimeter sets a bit in
        the auxiliary error register. The AUXERR? command returns a number
        representing the decimal-weighted sum of all set bits.The register is then cleared.

        The auxiliary error conditions and their weighted values are:\n
        1 Slave processor not responding\n
        2 DTACK failure\n
        4 Slave processor self-test failure\n
        8 Isolator test failure\n
        16 A/D converter convergence failure\n
        32 Calibration value out of range\n
        64 GPIB chip failure\n
        128 UART failure\n
        256 Timer failure\n
        512 Internal overload\n
        1024 ROM checksum failure, low-order byte\n
        2048 ROM checksum failure, high-order byte\n
        4096 Nonvolatile RAM failure\n
        8192 Option RAM failure\n
        16384 Cal RAM write or protection failure\n

        Remarks:
            - The auxiliary error register indicates hardware related errors. If one or more bits
            are set, the multimeter needs calibration or repair.\n
            - The AUXERR? command returns a 0 if no error bits are set.\n
            - If any bit in the auxiliary error register is set, the multimeter sets bit 0
            (hardware error) in the error register. Reading the auxiliary error register does
            not clear bit 0 in the error register. You must read the error register (ERR?
            command) to clear it.\n
            - Bits in the auxiliary error register cannot be masked to prevent them from
            setting bit 0 in the error register.\n

        Returns:
            str: auxiliary error.
        """
        return self.__get_data(f'AUXERR?')
    
    def set_beeper_enabled(self, state = 'ON') -> bool:
        """Controls the multimeter's beeper. When enabled, the beeper emits a 1 kHz beep if
        an error occurs.

        Args:
            state (str, optional): ON (0 Beeper enabled), OFF (1 Beeper disabled) and ONCE (2 Beeps once, then returns to previous mode (either OFF or ON)). Defaults to 'ON'.

        Returns:
            bool: status
        """
        if state == 'ON' or state == 'OFF' or state == 'ONCE':
            return self.__write_data(f'BEEP {state}')
        else:
            return False
    
    def call_subroutine(self, name) -> bool:
        """Call subprogram. Executes a previously stored subprogram.

        Args:
            name (str): Subprogram name. A subprogram name may contain up to 10 characters. The
            name can be alpha, alphanumeric, or an integer in the range of 0 to 127. Refer to
            the SUB command for details.

        Remarks:
            - Subprograms are created with the SUB command.\n
            - The multimeter sets bit 0 in the status register after executing a stored
            subprogram.\n
            - From the front panel, you can view all stored subprogram names by accessing
            the CALL command and pressing the up or down arrow key. Once you have
            found the correct subprogram, press the Enter key to execute the subprogram.\n

        Returns:
            bool: status
        """
        return self.__write_data(f'CALL {name}')
    
    def get_calibration_count(self) -> str:
        """Calibration number query. Returns an integer indicating the number of times the
        multimeter has been calibrated.

        Remarks:
            - The calibration number is incremented by 1 whenever the multimeter is
            calibrated. If autocal is secured, the calibration number is also incremented by
            1 whenever an autocal is performed; if unsecured, autocal does not affect the
            calibration number.\n
            - The calibration number is stored in cal-protected memory and is not lost when
            power is removed.\n
            - The multimeter was calibrated before it left the factory. When you receive the
            multimeter, read the calibration number to determine its initial value.\n

        Returns:
            str: calibration count.
        """
        return self.__get_data(f'CALNUM?')
    
    def set_calibration_string_nvram(self, string, sec_code=None) -> bool:
        """Calibration string (remote only). Stores a string in the multimeter's nonvolatile
            calibration RAM. Typical uses for this string include the multimeter's internal
            temperature at the time of calibration (TEMP? command), date of calibration,
            technician's name, and the scheduled date for the next calibration.

        Args:
            string (str): This is the alpha/numeric message that will be appended to the calibration RAM.
            The string parameter must be enclosed in single or double quotes. The maximum
            string length is 75 characters (the quotes enclosing the string are not counted as
            characters). 
            sec_code (str, int, optional):  When the calibration RAM is secured (SECURE command) you must include the
            security_code in order to write a message to the calibration RAM. (You can always
            read the string using the CALSTR? command regardless of the security mode).
            Refer to the SECURE command for information on securing and unsecuring the
            calibration RAM.. Defaults to None.

        Returns:
            bool: status
        """
        if sec_code is None:
            return self.__write_data(f'CALSTR {string}')
        else:
            return self.__write_data(f'CALSTR {string},{sec_code}')
        
    def get_calibration_string_nvram(self) -> str:
        """Calibration string query. Returns the string stored in the multimeter's nonvolatile
            calibration RAM.

        Returns:
            str: calibration string.
        """
        return self.__get_data(f'CALSTR?')
    
    def compress_subprogram(self, name)  -> bool:
        """Compress subprogram. Removes the ASCII text of a specified subprogram
            previously stored in memory. This saves memory space but removes the
            subprogram from continuous memory (the subprogram will be destroyed when
            power is removed).

        Args:
            name (str): Subprogram name. A subprogram name may contain up to 10 characters. The
            name can be alpha. alphanumeric, or an integer in the range of 0 to 127. Refer to
            the SUB command for details.

        Remarks:
            - To avoid memory fragmentation, compress each subprogram before
            downloading other subprograms.\n
            - You cannot store the COMPRESS command as part of a subprogram.\n

        Returns:
            bool: status
        """
        return self.__write_data(f'COMPRESS {name}')
    
    def continue_subprogram(self) -> bool:
        """Resumes execution of a subprogram that has been suspended by a
            PAUSE command.

        Remarks:
            - The GPIB Group Execute Trigger function may also be used to resume
            execution of a suspended subprogram.\n
            - Only one subprogram will be preserved in a suspended state. If a subprogram
            is paused and another is run which also becomes paused, the first will be
            terminated and the second will remain suspended.\n

        Returns:
            bool: status
        """
        return self.__write_data(f'CONT')
    
    def clear_status_byte(self) -> bool:
        """Clears (sets to 0) all bits in the status register.

        Remarks:
            - If a condition that set a bit in the status register still exists, that bit will be set
            again immediately after the CSB command is executed.\n
            - When you clear bit 6 (service requested), the multimeter sets the GPIB SRQ
            line false.\n

        Returns:
            bool: status
        """
        return self.__write_data(f'CSB')
    
    def set_multimeter_input_protection(self, mode='ON') -> bool:
        """Enables or disables the multimeter's input protection algorithm (see CAUTION
            below) and some syntax and error checking algorithms. With these algorithms
            disabled, the multimeter can change to a new measurement configuration faster
            than it can with them enabled.

        Args:
            mode (str, optional): ON (0 Input protection enabled) and OFF (1 Input protection disabled). Defaults to 'ON'.

        Caution:
            DEFEAT ON must only be used when you are certain that overload voltages
            on the Input terminals will not exceed ±100 V peak on the 10 V range or
            below. (On the 100 V and 1000 V ranges, the multimeter can withstand
            voltages up to ±1200 V peak regardless of whether DEFEAT is ON or OFF.)
            DEFEAT ON disables (defeats) the input switch sequencing that protects the
            multimeter's input circuitry from overload voltages. If input protection is
            disabled and an overload situation is detected on the 10 V range or below,
            the multimeter will enable input protection and internally tally the overload
            for instrument warranty considerations.

        Remarks:
            - Since DEFEAT ON disables certain syntax checking and error reporting
            algorithms, it should be used only after all system programming is complete
            and operational.

        Returns:
            bool: status
        """
        if mode == 'ON' or mode == 'OFF':
            return self.__write_data(f'DEFEAT {mode}')
        else:
            return False
        
    def get_multimeter_input_protection(self) -> str:
        """Returns the multimeter's input protection setting.

        Returns:
            str: input protection setting.
        """
        return self.__get_data(f'DEFEAT?')
    
    def set_user_defined_key(self, number, string) -> bool:
        """Allows you to assign one or more commands to a particular
            user-defined function key on the front panel (these keys are labeled f0 - f9). After
            assigning one or more commands to a key, pressing that key displays the
            command(s) on the multimeter's display. Pressing the Enter key will then execute
            the command(s) in the order listed. The DEFKEY DEFAULT command erases the
            strings assigned to all user-defined keys.

        Args:
            number (int, str): The number parameter is an integer in the range 0 - 9 (or F0 - F9) that designates
            the particular function key. \n
            string (str): The string parameter is the command or list of commands to be assigned to the
            function key. (Link multiple commands with a semicolon.) The string parameter
            must be enclosed in single or double quotes. The maximum string length is
            40 characters (the quotes enclosing the string are not counted as characters).

        Returns:
            bool: status
        """
        if (number >= 0 and number <= 9) or (number in ['F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9']):
            return self.__write_data(f'DEFKEY {number},{string}')
        elif string == 'DEFAULT':
            return self.__write_data(f'DEFKEY {string}')
        else:
            return False
        
    def get_user_defined_key(self, number) -> str: 
        """Returns the command or list of commands assigned to a particular user-defined
            function key.

        Args:
            number (int, str): The number parameter is an integer in the range 0 - 9 (or F0 - F9) that designates
            the particular function key.

        Remarks:
            - Key definitions stored from the front panel can be edited from the front panel.
            Definitions stored from remote cannot be edited.\n
            - You cannot embed quotes in the DEFKEY string. This means you cannot use
            the DISP command with a message in quotation marks as a string parameter.
            You can, however, use the DISP command and an unquoted message (refer to
            the DISP command for limitations on unquoted messages).\n

        Returns:
            str: command or list of commands.
        """
        if (number >= 0 and number <= 9) or (number in ['F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9']):
            return self.__get_data(f'DEFKEY? {number}')
        else:
            return False
        
    def set_delay_trig_sample(self, time) -> bool:
        """The DELAY command allows you to specify a time interval that is inserted
            between the trigger event and the first sample event.

        Args:
            time (int): Specifies the delay time in seconds. Delay time can range from 1E-7 (100 ns) to
            6000 seconds in 10 ns increments for direct- or sub-sampling (DSAC, DSDC,
            SSAC, or SSDC) or 100 ns increments for all other measurement functions.
            Specifying 0 for the delay sets the delay to its minimum possible value.

        Remarks:
            - The default delay changes automatically (unless you have specified an
            alternate value) whenever you change the measurement function (DCV, ACV,
            etc.), the range, the resolution, or the AC bandwidth setting (ACBAND
            command).\n

        Returns:
            bool: status
        """
        if time >= 0 and time <= 6000:
            return self.__write_data(f'DELAY {time}')
        else:
            return False
        
    def get_delay_trig_sample(self) -> str:
        """Returns the delay time in seconds.

        Returns:
            str: delay time.
        """
        return self.__get_data(f'DELAY?')
    
    def delete_subprogram(self, name) -> bool:
        """Delete subprogram. Removes a single subprogram from memory.

        Args:
            name (str): Subprogram name. A subprogram name may contain up to 10 characters. The
            name can be alpha, alphanumeric, or an integer in the range of 0 to 127. Refer to
            the SUB command for details.

        Remarks:
            - When a subprogram is deleted, the memory used to store it is freed and may
            be used to store a new subprogram (see the SUB command).\n
            - To delete all subprograms at once, use the SCRATCH command.\n

        Returns:
            bool: status
        """
        return self.__write_data(f'DELSUB {name}')
    
    def set_display_enabled(self, state, msg = None) -> bool:
        """Display. Enables or disables the multimeter's display, and may also be used to
            send a message to the display or to clear the display.

        Args:
            state (str): The state parameter choices are:'\n
            - OFF (0) Displays message if included (if no message, dashes are
            displayed); inactivates all annunciators except ERR; readings are
            no longer displayed and the display is not updated except to
            service front panel keystrokes and query commands.\n
            - ON (1) Normal (power-on mode) display operation.\n
            - MSG (2) Displays message, annunciators activated.\n
            - CLR (3) Clears the display.\n

            msg (str): The message parameter is the message to be displayed. The message may
            contain spaces, numerals, lower or upper case letters, and any of the following
            characters: ! # $ % & ' ( ) ^ \ / @ ; : [ ] , . + - = * < > ? _\n

        Remarks:
            - You must enclose a message in quotation marks only if it contains a space,
            comma, or semicolon. Either single or double marks (' or ") may be used: the
            beginning and ending marks must match.\n
            - A message may contain up to 75 characters (quotes enclosing the message
            are not counted as characters).\n

        Returns:
            bool: status
        """
        if state in ['OFF', 'ON', 'CLR'] and msg is None:
            return self.__write_data(f'DISP {state}')
        elif state == 'OFF' and msg is not None:
            return self.__write_data(f'DISP {state},{msg}')
        elif state == 'MSG':
            return self.__write_data(f"DISP {state},'{msg}'")
        else:
            return False
        
    def get_display_enabled(self) -> str:
        """Returns the display setting.

        Returns:
            str: display setting.
        """
        return self.__get_data(f'DISP?')
    
    def set_error_mask(self, mask) -> bool:
        """Error mask. The ERRMASK command allows you to mask (disable) certain bits in the
            error register. When a bit is masked, the multimeter will not set the corresponding
            bit in the error register. The error mask is cleared when power is removed.

        Args:
            mask (int): You enable an error condition by specifying its decimal weight as the value
            parameter. To enable more than one error condition, specify the sum of the
            weights. The error conditions and their weights are:
            -1 Hardware error (see AUXERR? for more information)\n
            -2 Calibration error\n
            -4 Trigger too fast error\n
            -8 Syntax error\n
            -16 Command not allowed from remote (ADDRESS command)\n
            -32 Undefined parameter received\n
            -64 Parameter out of range\n
            -128 Memory error\n
            -256 Destructive overload detected\n
            -512 Out of calibration\n
            -1024 Calibration required\n
            -2048 Settings conflict (memory improperly configured for sub-sampling)\n
            -4096 Math error (divide by 0, integer overflow, etc.)\n
            -8192 Subprogram error (calling a deleted sub, CONT with no PAUSE, SUBEND or
            PAUSE only allowed in sub, SCRATCH, DELSUB, CONT, not allowed in sub)\n
            -16384 System error (internal error, not user correctable)\n

        Remarks:
            - When an error occurs, it sets the corresponding bit in the error register
            regardless of whether or not it has been enabled by the EMASK command.
            Disabling an error bit prevents it from setting the error bit in the status register
            only, and thereby generating a service request.\n

        Returns:
            bool: status
        """
        return self.__write_data(f'EMASK {mask}')
    
    def get_error_mask(self) -> str:
        """Returns the error mask.

        Returns:
            str: error mask.
        """
        return self.__get_data(f'EMASK?')
    
    def set_end_of_identify(self, state) -> bool:
        """The END command enables or disables the GPIB End Or Identify (EOI) function.

        Args:
            state (str): The state parameter choices are:\n
                - OFF (0) EOI line never set true\n
                - ON (1) For multiple readings (SWEEP or NRDGS >1) the EOI line is set
                true with the last byte of the last reading sent. For single readings,
                EOI line set true with the last byte of each reading.\n
                - ALWAYS (2) EOI line set true when the last byte of each reading sent.\n

        Remarks:
            - Each reading output to the GPIB in ASCII format is normally followed by cr,lf
            (carriage return, line feed). The cr lf indicates the end of transmission 
            to mostcontrollers. Readings output in any other format do not have the cr lf end of
            line sequence. When using the ASCII output format and multiple readings are
            recalled from reading memory using the RMEM command, the multimeter
            places a comma between readings. In this case, the cr,lf occurs only once,
            following the last reading in the group being recalled. Commas are not used
            when readings are output directly to the bus (reading memory disabled), when
            readings are recalled using “implied read”, or when using any other output
            format.\n
            - Check your computer manual for information on how your computer responds
            to the EOI line.\n
            - If END ALWAYS is specified for the high-speed mode, the EOI mode
            automatically becomes ON while the readings are being taken. Following
            completion of the readings, the EOI mode returns to ALWAYS.\n

        Returns:
            bool: status
        """
        if state == 'ON' or state == 'OFF' or state == 'ALWAYS':
            return self.__write_data(f'END {state}')
        else:
            return False
        
    def get_end_of_identify(self) -> str:
        """Returns the EOI setting.

        Returns:
            str: EOI setting.
        """
        return self.__get_data(f'END?')
    
    def get_error(self) -> str:
        """When an error occurs, it sets a bit in the error register and illuminates
        the display's ERR annunciator. The ERR? command returns a number
        representing all set bits, clears the register, and shuts off the annunciator. The
        returned number is the weighted sum of all set bits.

        Error conditions and their weighted values are:\n
            - 1 Hardware error (see AUXERR? for more information)\n
            - 2 Calibration error\n
            - 4 Trigger too fast error\n
            - 8 Syntax error\n
            - 16 Command not allowed from remote (ADDRESS command)\n
            - 32 Undefined parameter received\n
            - 64 Parameter out of range\n
            - 128 Memory error\n
            - 256 Destructive overload detected\n
            - 512 Out of calibration\n
            - 1024 Calibration required\n
            - 2048 Settings conflict (memory improperly configured for sub-sampling)\n
            - 4096 Math error (divide by 0, integer overflow, etc.)\n
            - 8192 Subprogram error (calling a deleted sub, CONT with no PAUSE, SUBEND or
            PAUSE only allowed in sub, SCRATCH, DELSUB, CONT, not allowed in sub)\n
            - 16384 System error (internal error, not user correctable)\n

        Remarks:
            - The ERR? command returns a 0 if no error bits are set.\n
            - If bit 0 is set (weight = 1), refer to the auxiliary error register (AUXERR?
            command) for more information.\n
            - Executing the ERR? command clears the status register's error bit (bit 5).\n

        Returns:
            str: error register.
        """
        return self.__get_data(f'ERR?')
    
    def get_error_string(self) -> str:
        """The ERRSTR? command reads the least significant set bit in
            either the error register or the auxiliary error register and then clears the bit. The
            ERRSTR? command returns two responses separated by a comma. The first
            response is an error number (100 Series = error register; 200 Series = auxiliary
            error register) and the second response is a message (string) explaining the error.

        Remarks:
            - The maximum string length returned by ERRSTR? is 255 characters.\n
            - The ERRSTR? command reads and clears only the least significant set bit in a
            register. If more than one bit is set in a register, you must execute ERRSTR?
            repetitively to read and clear each set bit. After all set bits have been read and
            cleared (or if there were no set bits in either register), the ERRSTR? command
            returns 0,“NO ERROR”. When the auxiliary and error registers are cleared, the
            error bit in the status register (bit 5) will also be cleared.\n
            - When bit 0 in the error register is set, it means that one or more bits in the
            auxiliary error register are set. In this case, the ERRSTR? command reads and
            clears each set bit in the auxiliary error register first. When all auxiliary errors
            have been read, bit 0 in the error register is cleared and the ERRSTR?
            command can then be used to read any remaining errors in the error register.\n

        Returns:
            str: error message.
        """
        return self.__get_data(f'ERRSTR?')
    
    def set_external_output_event_trigger(self, event, polarity) -> bool:
        """External output event trigger. The EOT command configures the multimeter to
            generate a trigger event on the rear panel EXT TRIG connector. The trigger event
            can be used to synchronize the multimeter with other instruments or to trigger an
            external device.

        Args:
            event (str, int): The event parameter choices are:\n
                OFF (0) None; EXTOUT is disabled\n
                ICOMP (1) Input complete (1 μs pulse after A/D converter has integrated
                each reading or, for direct- or sub-sampling, after the track and
                hold has acquired the input signal)\n
                ONCE (2) Outputs a 1 μs pulse upon execution of the EXTOUT ONCE
                command; the event then becomes OFF\n
                APER (3) Aperture waveform (a level indicating when the A/D converter is
                making a measurement)\n
                BCOMP (4) Burst complete (1 μs pulse following a group of readings)\n
                SRQ (5) Status event occurred (1 μs pulse whenever a status register event
                occurs that has been enabled to assert the GPIB SRQ). (See
                second Remark below.)\n
                RCOMP (6) Reading complete (1 μs pulse after each reading)\n
            polarity (str): The polarity parameter choices are:\n
                - NEG (0) - Trigger event is negative.\n
                - POS (1) - Trigger event is positive.\n


        Remarks:
            - All events except APER generate a 1 μs pulse on the EXTOUT connector. If
            APER is selected, the A/D's aperture waveform is output directly. The leading
            edge of the EXTOUT signal is the response to the event.\n
            -When a status event sets the SRQ bit in the status register, that bit remains set
            until cleared (CSB command, for example). When specified, the EXTOUT SRQ
            pulse occurs whenever any status event occurs that has been enabled to
            assert SRQ (RQS command). The EXTOUT SRQ pulse does not necessarily
            occur whenever the SRQ bit is set; it occurs whenever an enabled status event
            occurs.\n

        Returns:
            bool: status
        """
        if event in ['OFF', 'ICOMP', 'ONCE', 'APER', 'BCOMP', 'SRQ', 'RCOMP'] and polarity in ['NEG', 'POS']:
            return self.__write_data(f'EXTOUT {event},{polarity}')
        else:
            return False
        
    def get_external_output_event_trigger(self) -> str:
        """Returns the external output event trigger setting.

        Returns:
            str: external output event trigger setting.
        """
        return self.__get_data(f'EXTOUT?')
    
    def set_input_buffer_enabled(self, control) -> bool:
        """Enables or disables the multimeter's input buffer. When enabled,
        the input buffer temporarily stores the commands it receives over the GPIB bus.
        This releases the bus immediately after a command is received, allowing the
        controller to perform other tasks while the multimeter executes the stored
        command.

        Args:
            control (str,int): The control parameter choices are:\n
                - OFF (0) Disables the input buffer; commands are accepted only when the
                multimeter is not busy\n
                - ON (1) Enables the input buffer; commands are stored, releasing the bus
                immediately\n

        Remarks:
            - Turning the input buffer OFF causes a minor degradation in speed
            performance, but is useful for synchronizing bus activity. With the input buffer
            OFF, the multimeter accepts only one command at a time and does not release
            the bus until it has finished executing that command. This ensures that
            subsequent commands sent to other bus devices cannot be executed until the
            multimeter has finished executing its command(s).\n
            - Turning the input buffer ON causes the multimeter to buffer (store) incoming
            messages and release the GPIB bus as soon as message transmission is
            complete. This allows the controller to communicate with other bus devices
            while the multimeter executes its command(s). However, synchronization with
            other bus devices may be lost if they execute their instructions before the
            multimeter finishes its instructions. In this case, the ready bit in the status
            register may be monitored (using a serial poll) to determine when the
            multimeter is finished.\n
            - A series of commands longer than 255 characters fills the input buffer and
            causes the multimeter to halt bus activity while it executes the first commands
            received. The remainder of the message is input when room becomes available
            in the buffer.\n

        Returns:
            bool: status
        """
        if control in ['OFF', 'ON']:
            return self.__write_data(f'INBUF {control}')
        else:
            return False
        
    def get_input_buffer_enabled(self) -> str:
        """Returns the input buffer setting.

        Returns:
            str: input buffer setting.
        """
        return self.__get_data(f'INBUF?')

    def get_line_frequency(self) -> str:
        """Measures and returns the frequency of the AC power line.

        Remarks:
            - Refer to the LFREQ command on the previous page for an example showing
            how to measure the line frequency and automatically set the A/D converter's
            reference frequency to the measured value.\n

        Returns:
            str: line frequency.
        """
        return self.__get_data(f'LINE?')
    
    def set_keypad_locked(self, control) -> bool:
        """Enables or disables the multimeter's keyboard.

        Args:
            control (str, int): The control parameter choices are:\n
                - OFF (0) Enables the keyboard (normal operation)\n
                - ON (1) Disables the keyboard (pressing keys has no affect)\n

        Remarks:
            - The LOCK command is accessible from the front panel's alphabetic command
            directory. However, executing the LOCK command from the front panel has no
            effect.\n
            - After disabling the keyboard, you can only enable it from the controller or by
            cycling power. The LOCK command disables the multimeter's Local key.\n

        Returns:
            bool: status
        """
        if control in ['OFF', 'ON']:
            return self.__write_data(f'LOCK {control}')
        else:
            return False
        
    def get_keypad_locked(self) -> str:
        """Returns the keyboard setting.

        Returns:
            str: keyboard setting.
        """
        return self.__get_data(f'LOCK?')
    
    def get_number_of_stored_readings(self) -> str:
        """Returns the total number of stored readings.

        Returns:
            str: number of readings.
        """
        return self.__get_data(f'MCOUNT?')
    
    def set_memory_storage_mode(self, mode) -> bool:
        """Enables or disables reading memory and designates the storage mode.

        Args:
            mode (str): The mode parameter choices are:\n
                - OFF (0) Stops storing readings (stored readings stay intact)\n
                - LIFO (1) Clears reading memory and stores new readings LIFO (last-in-first-out)\n
                - FIFO (2) Clears reading memory and stores new readings FIFO (first-in-first-out)\n
                - CONT (3) Keeps memory intact and selects previous mode (if there was no previous mode, FIFO is selected)\n

        Remarks:
            - In the high-speed mode, when reading memory is enabled in the FIFO mode
            and becomes full, the trigger arm event becomes HOLD which stops readings
            and removes the multimeter from the high-speed mode. After removing some
            or all of the readings from memory, you can resume measurements by
            changing the trigger arm event (TARM command). When not in the high-speed
            mode, when you fill memory in the FIFO mode, the stored readings remain
            intact and new readings are not stored. In the LIFO mode, when reading
            memory becomes full, the oldest readings are replaced with the newest
            readings regardless of whether in the high-speed mode or not.\n
            - When the controller requests data from the multimeter and its output buffer is
            empty in the LIFO or FIFO mode, a reading is removed from memory and sent
            to the controller. This is the “implied read” method of recalling readings. In the
            LIFO mode, the most recent reading is returned. In the FIFO mode, the oldest
            reading is returned. The reading storage mode (LIFO or FIFO) is important only
            when you are using the “implied read” method of recalling readings. The
            reading storage mode has no effect on readings recalled using the RMEM
            command.\n
            - Use the MFORMAT command to specify the memory format (SINT, DINT, ASCII,
            SREAL, or DREAL).\n
            - Executing the RMEM command sets reading memory to OFF. You must
            execute MEM CONT, MEM FIFO, or MEM LIFO to re-enable reading memory
            after executing RMEM.\n
        
        Returns:
            bool: status
        """
        if mode in ['OFF', 'LIFO', 'FIFO', 'CONT']:
            return self.__write_data(f'MEM {mode}')
        else:
            return False
    
    def get_memory_storage_mode(self) -> str:
        """Returns the memory storage mode.

        Returns:
            str: memory storage mode.
        """
        return self.__get_data(f'MEM?')
    
    def set_command_meny_mode(self, mode) -> bool:
        """The MENU command selects the SHORT or FULL list of commands in the front
            panel's alphabetic command menu.
            
            Args:
                mode (str): The mode parameter choices are:\n
                    - SHORT (0) Selects the short command menu\n
                    - FULL (1) Selects the full command menu\n

            Remarks:
                - To access the alphabetic command menu, press any of the shifted MENU keys
                labeled C, E, L, N, R, S, and T. You can then locate a particular command using
                the up and down arrow keys.\n
                - The mode parameter is stored in continuous memory (not lost when power is
                removed).\n
                - The FULL menu contains all commands except query commands that can be
                made by accessing a command and appending a question mark (e.g., BEEP,
                BEEP?). The SHORT menu eliminates the GPIB bus-related commands and any
                commands that have dedicated front panel keys (e.g., RSTATE command,
                Recall State key).\n

            Returns:
                bool: status 
            """
        if mode in ['SHORT', 'FULL']:
            return self.__write_data(f'MENU {mode}')
        else:
            return False
        
    def get_command_menu_mode(self) -> str:
        """Returns the command menu mode.

        Returns:
            str: command menu mode.
        """
        return self.__get_data(f'MENU?')
    
    def get_total_memory(self) -> str:
        """The MSIZE? query command, however, is
            useful to determine the total reading memory and the largest unused block of
            subprogram/state memory.

        Remarks:
            - As subprogram/state memory is used, it eventually becomes fragmented into
            many small blocks. The MSIZE? command returns the total number of bytes of
            reading memory and the number of bytes of the largest unused block of
            subprogram/state memory. The SCRATCH command clears all subprograms
            and states from memory returning these memory areas to one contiguous
            block. Also, when power is cycled, the multimeter combines fragmented
            blocks of memory wherever possible.\n

        Returns:
            str: total memory.
        """
        return self.__get_data(f'MSIZE?')
    
    def set_number_of_digits(self, value) -> bool:
        """Designates the number of digits to be displayed by the multimeter.

        Args:
            value (int): The value parameter can be an integer from 3 to 8 (there is an implied 1/2 digit;
            that is, when you specify NDIG 3, the multimeter displays 3 1/2 digits.)

        Remarks:
            - The NDIG command sets the maximum number of digits displayed. It does not
            affect the A/D converter's resolution or readings sent to memory or the GPIB
            bus. The multimeter cannot display more digits than are resolved by the A/D
            converter.\n

        Returns:
            bool: status
        """
        if value >= 3 and value <= 8:
            return self.__write_data(f'NDIG {value}')
        else:
            return False
        
    def get_number_of_digits(self) -> str:
        """Returns the number of digits setting.

        Returns:
            str: number of digits.
        """
        return self.__get_data(f'NDIG?')
    
    def set_number_of_reading_per_trigger(self, count, event='AUTO') -> bool:
        """Designates the number of readings taken per trigger and
            the event (sample event) that initiates each reading.

        Args:
            count (int): Designates the number of readings per trigger event. The valid range for this
            parameter is 1 to 16777215. (The count parameter also corresponds to the record
            parameter in the RMEM command. Refer to the RMEM command for details.)\n
            event (str): Designates the event that initiates each reading (sample event). The event
            parameter choices are:\n
                - AUTO (1) Initiates reading whenever the multimeter is not busy\n
                - EXTSYN (2) Initiates reading on negative edge transition on the multimeter's
                external trigger input connector\n
                - SYN (5) Initiates reading when the multimeter's output buffer is empty,
                reading memory is off or empty, and the controller requests data.\n
                - TIMER (6) Similar to AUTO with a time interval between successive readings
                (specify interval with the TIMER command). Cannot be used for sampled AC or AC+DC voltage measurements (SETACV RNDM or
                SYNC) or for frequency or period measurements.\n
                - LEVEL (7) Initiates reading when the input signal reaches the voltage
                specified by the LEVEL command on the slope specified by the
                SLOPE command. Can be used only for DC voltage and direct-sampled measurements.\n
                - LINE (8) Initiates reading on a zero crossing of the AC line voltage. Cannot be used for sampled AC or AC+DC voltage measurements (SETACV RNDM or
                SYNC) or for frequency or period measurements.\n

        Remarks:
            - Since the TIMER event designates an interval between readings, it only applies
            when count is greater than one. The first reading occurs without the TIMER
            interval. However, you can insert a time interval before the first reading with
            the DELAY command. (The TIMER event suspends autoranging.)\n
            - You can use the SWEEP command to replace the two commands: NRDGS
            n,TIMER and TIMER n. The SWEEP command specifies the number of readings
            and the interval between readings. These commands are interchangeable; the
            multimeter uses whichever command was executed last in the programming.
            Executing the SWEEP command automatically sets the sample event to
            TIMER. In the power-on, RESET, and PRESET states, the multimeter uses the
            NRDGS command.\n
            - When SYN is used for more than one of the trigger arm, trigger, or sample
            events, a single occurrence of the SYN event satisfies all of the specified SYN
            event requirements. This is shown in the second “SYN event” example below.\n

        Returns:
            bool: status
        """
        if event in ['AUTO', 'EXTSYN', 'SYN', 'TIMER', 'LEVEL', 'LINE'] and count >= 1 and count <= 16777215:
            return self.__write_data(f'NRDGS {count},{event}')
        else:
            return False
        

    def get_multimeter_installed_options(self) -> str:
        """Returns the installed options.\n
            0 = No installed options\n
            1 = Extended Reading Memory Option\n

        Returns:
            str: installed options.
        """
        return self.__get_data(f'OPT?')
    
    def suspend_subprogram(self) -> bool:
        """Suspends subprogram execution. The subprogram can be resumed using the
        CONT command or by executing the GPIB Group Execute Trigger command.

        Remarks:
            - The PAUSE command is allowed only within a subprogram.\n
            - Only one subprogram will be preserved in a suspended state. If a subprogram
            is paused and another is run which also becomes paused, the first will be
            terminated and the second will remain suspended.\n
            - With the input buffer off (INBUF OFF command), the GPIB bus is normally held
            by the multimeter until a called subprogram is completely executed. If a
            PAUSE command is encountered in a subprogram, the GPIB bus is released
            immediately.\n
            - Nested PAUSE commands are not allowed; that is, when a subprogram is
            called from another subprogram, the called subprogram cannot contain a
            PAUSE command.\n

        Returns:
            bool: status
        """
        return self.__write_data(f'PAUSE')
    
    def set_predefined_state(self, state) -> bool:
        """Configures the multimeter to one of three predefined states.

        Args:
            state (int): Specifies the NORM, FAST, or DIG preset state (the numeric query equivalents of
            these parameters are 1, 0, and 2, respectively).

        NORMAL (NORM) state:\n
            PRESET NORM is similar to RESET but optimizes the multimeter for remote
            operation. Executing PRESET NORM executes the following commands:\n
            ACBAND 20,2E+6MEM OFF (last memory operation set to FIFO)\n
            AZERO ONMFORMAT SREAL\n
            BEEP ONMMATH OFF\n
            DCV AUTONDIG 6\n
            DELAY -1NPLC 1\n
            DISP ONNRDGS 1,AUTO\n
            FIXEDZ OFF OCOMP OFF\n
            FSOURCE ACVOFORMAT ASCII\n
            INBUF OFFTARM AUTO\n
            LOCK OFFTIMER 1\n
            MATH OFFTRIG SYN\n
            All math registers set to 0 except:\n
            DEGREE = 20\n
            PERC = 1\n
            REF = 1\n
            RES = 50\n
            SCALE = 1\n

        FAST state:\n
            PRESET FAST configures the multimeter for fast readings, fast transfer to
            memory, and fast transfer from memory to GPIB. (Refer to Increasing the Reading
            Rate in Chapter 4 for more information on fast measurements.) Executing PRESET
            FAST executes the commands shown under PRESET NORM with the following
            exceptions:\n
            DCV 10\n
            AZERO OFF\n
            DISP OFF\n
            MFORMAT DINT\n
            OFORMAT DINT\n
            TARM SYN\n
            TRIG AUTO\n

        DIG (DIGITIZE) state:\n
            PRESET DIG configures the multimeter for DCV digitizing (DCV digitizing is
            discussed in Chapter 5). Executing PRESET DIG executes the commands shown
            under PRESET NORM with the following exceptions:\n
            DCV 10\n
            AZERO OFF\n
            DELAY 0\n
            DISP OFF\n
            TARM HOLD\n
            TRIG LEVEL\n
            LEVEL 0,AC\n
            NRDGS 256,TIMER\n
            TIMER 20E-6\n
            APER 3E-6\n
            MFORMAT SINT\n
            OFORMAT SINT\n

        Returns:
            bool: status
        """
        if state in ['NORM', 'FAST', 'DIG']:
            return self.__write_data(f'PRESET {state}')
        else:
            return False
        
    def get_predefined_state(self) -> str:
        """Returns the predefined state.

        Returns:
            str: predefined state.
        """
        return self.__get_data(f'PRESET?')
    
    def remove_single_state_from_memory(self, name) -> bool:
        """Removes a single stored state from memory.

        Args:
            name (str):State name. A state name may contain up to 10 characters. The name can be
            alpha, alphanumeric, or an integer in the range of 0 to 127. Refer to the SSTATE
            command for details.

        Remarks:
            - To delete all states at once, use the SCRATCH command.\n

        Returns:
            bool: status
        """
        return self.__write_data(f'REMST {name}')

    def set_query_responses_setting(self, type) -> bool:
        """Designates whether query responses contain numeric or alpha
            characters (whenever possible), and whether command headers are returned.

        Args:
            type (str): The type parameter choices are:\n
                - NUM (0) Query responses sent to either GPIB or the display are numeric
                only (whenever possible) with no headers\n
                - NORM (1) Query responses sent to the GPIB are numeric only (whenever
                possible) with no headers; query responses sent to the display
                contain alpha headers and alpha responses (whenever possible)\n
                - ALPHA Query responses sent to either GPIB or the display contain an
                alpha header and an alpha response (whenever possible)\n

        Remarks:
            - The numeric query equivalents for alpha parameters are shown under each
            applicable command in this chapter. Some query commands such as DEFKEY?
            will always return alpha characters regardless of the specified QFORMAT.
            Similarly, some query commands such as NDIG? will always return a numeric
            response.\n
            - When you execute a query command from the multimeter's front panel, the
            result goes to the display only. When you execute a query command from the
            controller, the result goes to the multimeter's output buffer only. Query results
            are returned in ASCII format, after which the output format returns to the
            previously specified type (ASCII, SINT, etc.).\n

        Returns:
            bool: status
        """
        if type in ['NUM', 'NORM', 'ALPHA']:
            return self.__write_data(f'QFORMAT {type}')
        else:
            return False
        
    def get_query_responses_setting(self) -> str:
        """Returns the query response setting.

        Returns:
            str: query response setting.
        """
        return self.__get_data(f'QFORMAT?')
    
    def set_range(self, max_input, perc_resolution=None) -> bool:
        """Designates the range and resolution for the multimeter.

        Args:
            max_input (float): The max._input parameter selects a fixed range or the autorange mode. To select
            a fixed range, you specify the max._input as the absolute value (no negative
            numbers) of the maximum expected amplitude of the input signal. The multimeter
            then selects the correct range. To select the autorange mode, specify AUTO for
            max._input or default the parameter. In the autorange mode, the multimeter
            samples the input signal before each reading and selects the appropriate range.\n
            For DCV:\n
            max_input -1 or AUTO range autorange\n
            max_input 0 to 0.12 range 100 mV full scale 120 mV\n
            max_input from 0.12 to 1.2 range 1 V full scale 1.2 V\n
            max_input from 1.2 to 12 range 10 V full scale 12 V\n
            max_input from 12 to 120 range 100 V full scale 120 V\n
            max_input from 120 to 1E3 range 1000 V full scale 1050 V\n
            
            For ACV or ACDCV:\n
            max_input -1 or AUTO range autorange\n
            max_input 0 to 0.012 range 10 mV full scale 12 mV\n
            max_input from 0.012 to 0.12 range 100 mV full scale 120 mV\n
            max_input from 0.12 to 1.2 range 1 V full scale 1.2 V\n
            max_input from 1.2 to 12 range 10 V full scale 12 V\n
            max_input from 12 to 120 range 100 V full scale 120 V\n
            max_input from 120 to 1E3 range 1000 V full scale 1050 V\n

            For OHM or OHMF:\n
            max_input -1 or AUTO range autorange\n
            max_input 0 to 12 range 10 Ω full scale 12 Ω\n
            max_input from 12 to 120 range 100 Ω full scale 120 Ω\n
            max_input from 120 to 1E3 range 1 kΩ full scale 1.2 kΩ\n
            max_input from 1E3 to 12 range 10 kΩ full scale 12 kΩ\n
            max_input from 12 to 120 range 100 kΩ full scale 120 kΩ\n
            max_input from 120 to 1E6 range 1 MΩ full scale 1.2 MΩ\n
            max_input from 1E6 to 12 range 10 MΩ full scale 12 MΩ\n
            max_input from 12 to 120 range 100 MΩ full scale 120 MΩ\n
            max_input from 120 to 1E9 range 1 GΩ full scale 1.2 GΩ\n

            For DCI:\n
            max_input -1 or AUTO range autorange\n
            max_input 0 to 0.12E-6 range 100 nA full scale 120 nA\n
            max_input from 0.12E-6 to 1.2E-6 range 1 μA full scale 1.2 μA\n
            max_input from 1.2E-6 to 12E-6 range 10 μA full scale 12 μA\n
            max_input from 12E-6 to 120E-6 range 100 μA full scale 120 μA\n
            max_input from 120E-6 to 1.2E-3 range 1 mA full scale 1.2 mA\n
            max_input from 1.2E-3 to 12E-3 range 10 mA full scale 12 mA\n
            max_input from 12E-3 to 120E-3 range 100 mA full scale 120 mA\n
            max_input from 120E-3 to 1.2 range 1 A full scale 1.05 A\n

            For ACI or ACDCI:\n
            max_input -1 or AUTO range autorange\n
            max_input 0 to 120E-6 range 100 μA full scale 120 μA\n
            max_input from 120E-6 to 1.2E-3 range 1 mA full scale 1.2 mA\n
            max_input from 1.2E-3 to 12E-3 range 10 mA full scale 12 mA\n
            max_input from 12E-3 to 120E-3 range 100 mA full scale 120 mA\n
            max_input from 120E-3 to 1.2 range 1 A full scale 1.05 A\n

            For SSAC or SSDC:\n
            0 to 0.012 range 10 mV full scale 12 mV\n
            from 0.012 to 0.12 range 100 mV full scale 120 mV\n
            from 0.12 to 1.2 range 1 V full scale 1.2 V\n
            from 1.2 to 12 range 10 V full scale 12 V\n
            from 12 to 120 range 100 V full scale 120 V\n
            from 120 to 1E3 range 1000 V full scale 1050 V\n

            For DSAC or DSDC:\n
            0 to 0.012 range 10 mV full scale SINT format 12 mV DINT format 50 mV \n
            from 0.012 to 0.12 range 100 mV full scale SINT format 120 mV DINT format 500 mV \n
            from 0.12 to 1.2 range 1 V full scale SINT format 1.2 V DINT format 5 V \n
            from 1.2 to 12 range 10 V full scale SINT format 12 V DINT format 50 V \n
            from 12 to 120 range 100 V full scale SINT format 120 V DINT format 500 V \n
            from 120 to 1E3 range 1000 V full scale SINT format 1050 V DINT format 1050 V \n

            perc_resolution (float): For all functions except the digitizing functions (DSAC. DSDC, SSAC, and SSDC),
            the %_resolution parameter specifies the measurement resolution. (The
            multimeter ignores %_resolution when included with a digitizing command.) For
            frequency and period measurements, you specify %_resolution as the number of
            digits to be resolved. For the remaining measurement functions (DCV, ACV,
            ACDCV, OHM, OHMF, DCI, and ACI), you specify the %_resolution as a percentage
            of the max._input parameter. The multimeter then multiplies %_resolution by the
            max._input to determine the measurement's resolution.

        Note: When using autorange, the multimeter multiplies the %_resolution parameter
        times the full scale reading of the selected range. The result is the minimum
        resolution. The multimeter always gives you at least the minimum resolution
        and, in many cases, gives you additional digits of resolution.
    
        Returns:
            bool: status
        """

        if perc_resolution is None and max_input >= 0:
            return self.__write_data(f'RANGE {max_input}')
        elif perc_resolution is not None and max_input >= 0:
            return self.__write_data(f'RANGE {max_input},{perc_resolution}')
        else:
            return False
        
    def get_range(self) -> str:
        """Returns the range setting.

        Returns:
            str: range setting.
        """
        return self.__get_data(f'RANGE?')
    
    def set_reading_reasolution(self, perc_res) -> bool:
        """Specifies reading resolution.

        Args:
            perc_res (float): For frequency and period measurements, the %_resolution parameter specifies
            the digits of resolution and the gate time as shown below. (%_resolution also
            affects the reading rate.) If you default the %_resolution parameter for frequency or
            period measurements, the multimeter uses .00001.

            for perc_res .00001 gate time is 1 s and digit resolution is 7
            for perc_res .0001 gate time is 0.1 s and digit resolution is 7
            for perc_res .001 gate time is 0.01 s and digit resolution is 6
            for perc_res .01 gate time is 0.001 s and digit resolution is 5
            for perc_res .1 gate time is 0.0001 s and digit resolution is 4


            For sampled ACV or ACDCV, random sampling (SETACV RNDM) has a fixed
            resolution of 4.5 digits that cannot be changed. For synchronous sampling
            (SETACV SYNC), a %_resolution parameter of 0.001 = 7.5 digits; 0.01 = 6.5 digits;
            0.1 = 5.5 digits; and 1= 4.5 digits.
            For all other functions (except DSAC, DSDC, SSAC, and SSDC): %_resolution is
            ignored for these functions), the multimeter multiplies %_resolution times the
            present measurement range (1 V, 10 V, 100 V, etc.) to determine the resolution. To
            compute the %_resolution parameter, use the equation:
            %_resolution = (actual resolution/range) × 100.
            For example, suppose you are measuring DC voltage on the 10 V range and you
            want 100 μV of resolution. The equation evaluates to:
            %_resolution = (.0001 /10) × 100 = .001
            Power-on %_resolution none. At power-on, the resolution is determined by the
            NPLC command which produces 8 ½ digits. (The power-on value for NDIG masks
            1 display digit causing the multimeter to display only 7 ½ digits. You can use the
            NDIG 8 command to display all 8 ½ digits.)

        Remarks:
            - For analog measurements, the %_resolution parameter of the RES command
            operates slightly differently than the %_resolution parameter of a function
            command (FUNC, ACV, DCV, etc.) or the RANGE command. When used with
            the RES command, %_resolution is multiplied times the range to determine
            the actual resolution. When used with a function command or the RANGE
            command, %_resolution is multiplied times that command's max._input
            parameter. The max._input parameter may or may not be the value of a
            measurement range.\n

        Returns:
            bool: status
        """
        return self.__write_data(f'RES {perc_res}')
    
    def get_reading_resolution(self) -> str:
        """Returns the reading resolution setting.

        Returns:
            str: reading resolution setting.
        """
        return self.__get_data(f'RES?')
    
    def reset_multimeter(self) -> bool:
        """Resets the multimeter to its power-on state without cycling power.
        Aborts readings in process.
        Clears error and auxiliary error registers.
        Clears the status register except the Power-on SRQ bit (bit 3).
        Clears reading memory.
        In addition, the RESET command also executes these commands:

        ACBAND 20,2E6\n
        AZERO ON\n
        DCV AUTO\n
        DEFEAT OFF\n
        DELAY -1\n
        DISP ON\n
        EMASK 32767 (all enabled)\n
        END OFF\n
        EXTOUT ICOMP,NEG\n
        FIXEDZ OFF\n
        FSOURCE ACV\n
        INBUF OFF\n
        LEVEL 0,AC\n
        LFILTER OFF\n
        LFREQ (line frequency rounded to 50 Hz or 60 Hz)\n
        LOCK OFF\n
        MATH OFF\n
        MEM OFF (last memory operation set to FIFO)\n
        MFORMAT SREAL\n
        MMATH OFF\n
        NDIG 7\n
        NPLC 10\n
        NRDGS 1,AUTO\n
        OCOMP OFF\n
        OFORMAT ASCII QFORMAT NORM\n
        RATIO OFF\n
        RQS 0\n
        SETACV ANA\n
        SLOPE POS\n
        SSRC LEVEL,AUTO\n
        ALL math registers set to 0 except:\n
        DEGREE = 20\n
        SCALE = 1\n
        PERC = 1\n
        REF = 1\n
        RES = 50\n

        Remark:
            - Although RESET can be used from remote, it is intended primarily for front
            panel use. RESET configures the multimeter to a good starting point for local
            operation. Executing the RESET command from the alphabetic menu resets
            the multimeter as shown above. Pressing the shifted front panel Reset key,
            however, has the same effect as cycling the multimeter's power. This stores
            the present state as state 0, any compressed subprograms are destroyed,
            stored readings are destroyed, the power-on SRQ bit is set in the status
            register, and the power-on sequence is performed.\n
            - When attempting to send the RESET command from remote, it is possible that
            the multimeter is busy or the GPIB bus is being held. In either case, the
            multimeter will not respond immediately to the remote RESET command. For
            this reason, you should send the GPIB device clear command before you send
            the multimeter's RESET command. This is shown in the example below.\n

        Returns:
            bool: status
        """
        return self.__write_data(f'RESET')
    
    def get_firmware_version(self) -> str:
        """Returns two numbers separated by a comma. The first number is
            the multimeter's master processor firmware revision. The second number is the
            slave processor firmware revision.

        Returns:
            str: firmware version.
        """
        return self.__get_data(f'REV?')
    
    def get_math_register(self, register) -> str:
        """Reads and returns the contents of a math register.

        Args:
            register(str,int): The register parameter choices are:\n
                - DEGREE (1) Time constant for FILTER and RMS\n
                - LOWER (2) Smallest reading in STATS\n
                - MAX (3) Upper Limit for PFAIL operation\n
                - MEAN (4) Average of readings in STATS\n
                - MIN (5) Lower limit for PFAIL\n
                - NSAMP (6) Number of samples in STATS\n
                - OFFSET (7) Subtrahend in NULL and SCALE operations\n
                - PERC (8) % value for PERC operation\n
                - REF (9) Reference value for DB operation\n
                - RES (10) Reference impedance for DBM operation\n
                - SCALE (11) Divisor in the SCALE operation\n
                - SDEV (12) Standard deviation in STATS\n
                - UPPER (13) Largest reading in STATS\n
                - HIRES (14) Not used by any math operation (extra register)\n
                - PFAILNUM (15) The number of reading that passed PFAIL before a failure was encountered\n

        Remarks:    
            - Math register contents are always output in the ASCII output format regardless
            of the specified output format. Afterwards, the output format returns to that
            previously specified (SINT, DINT, SREAL, DREAL, or ASCII).\n
                
        Returns:
            str: math register value.
        """
        if register in ['DEGREE', 'LOWER', 'MAX', 'MEAN', 'MIN', 'NSAMP', 'OFFSET', 'PERC', 'REF', 'RES', 'SCALE', 'SDEV', 'UPPER', 'HIRES', 'PFAILNUM']:
            return self.__get_data(f'RMATH {register}')
        else:
            return False
        
    def read_memory(self, first=1, count=1, record=1) -> str:
        """Reads and returns the value of a reading or group of readings
            stored in reading memory. RMEM leaves stored readings intact (not cleared from
            memory).

        Args:
            first (int): Designates the beginning reading.\n
            count (int): Designates the number of readings to be recalled, starting with first.\n
            record (int): Designates the record from which to recall readings. Records correspond to the
            number of readings specified by the NRDGS command. For example, if NRDGS
            specifies three readings per trigger, each record will contain three readings.\n

        Remarks:
            - The RMEM command automatically shuts off reading memory (MEM OFF). This
            means all previously stored readings remain intact and new readings are not
            stored. You can re-enable reading memory without destroying any stored
            readings using the MEM CONT command.\n
            - The multimeter assigns a number to each reading in reading memory. The
            most recent reading is assigned the lowest number (1) and the oldest reading
            has the highest number. Numbers are always assigned in this manner
            regardless of whether you're using the FIFO or LIFO mode. Records are also
            numbered in this manner—the most recent record is record number 1.\n
            - When you execute the RMEM command from the front panel, readings are
            copied, one at a time, to the display. After viewing the first reading, you can
            view others by using the up or down arrow key. Use the left and right arrow
            keys to view the reading number (left side of display) and the reading (right
            side of display).\n

        Returns:
            str: memory location value.
        """
        return self.__get_data(f'RMEM {first},{count},{record}')
    
    def set_request_service(self, value) -> bool:
        """Enables one or more status register conditions. When a
        condition is enabled and that condition occurs, it sets the GPIB SRQ line true.

        Args:
            value (int): You enable a condition by specifying its decimal weight as the value parameter.
            For more than one condition, specify the sum of the weights. The conditions and
            their weights are:\n
                - 1 Program Memory Execution Completed\n
                - 2 Hi or Lo Limit Exceeded\n
                - 4 SRQ Command Executed\n
                - 8 Power-On SRQ\n
                - 16 Ready for Instructions\n
                - 32 Error (Consult Error Register)\n
                - 64 Service Requested (you cannot disable this bit)\n
                - 128 Data Available\n

        Remarks:
            - You can control the errors that will set bit 5 with the EMASK command.\n
            - The power-on SRQ bit is stored in continuous memory. All other bits are
            cleared at power-on.\n

        Returns:
            bool: status
        """
        if value >= 0 and value <= 255:
            return self.__write_data(f'RQS {value}')
        else:
            return False
        
    def get_request_service(self) -> str:
        """Returns the request service setting.

        Returns:
            str: request service setting.
        """
        return self.__get_data(f'RQS?')
    
    def recall_state_from_memory(self, name) -> bool:
        """Recalls a stored state from memory and configures the multimeter to
            that state. States are stored using the SSTATE command.

        Args:
            name (str): State name. A state name may contain up to 10 characters. The name can be
            alpha, alphanumeric, or an integer in the range of 0 to 127. Refer to the SSTATE
            command for details.
        
        Remarks:
            - Whenever the multimeter's power is removed, the present state is stored in
            state 0. After a power failure, the multimeter can be configured to its previous
            state by executing RSTATE 0.\n
            - If the NULL real-time math operation was enabled in a stored state, after
            recalling the state, the first reading is placed in the OFFSET register (refer to
            NULL in Chapter 4 for more information).\n 
            - From the front panel, you can review the names of all stored states by pressing
            the Recall State key and by using the up and down arrow keys. When you have
            found the desired state, press the Enter key to recall that state.\n
        
        Returns:
            bool: status
        """
        return self.__write_data(f'RSTATE {name}')
    
    def clear_all_subprograms_and_states(self) -> bool:
        """Clears all subprograms and states from memory.

        Remarks:
            - Individual subprograms can be cleared with the DELSUB command. Individual
            states can be cleared with the PURGE command.\n

        Returns:
            bool: status
        """
        return self.__write_data(f'SCRATCH')
    
    def set_security_code(self, old, new, acal_code = 'OFF') -> bool:
        """Allows the person responsible for calibration to enter a security
        code to prevent accidental or unauthorized calibration or autocalibration
        (autocal). 

        Args:
            old (str): This is the multimeter's previous security code. The multimeter is shipped from
            the factory with its security code set to 3458A.\n
            new (str): This is the new security code. The code is an integer from -2.1E9 to 2.1E9. If the
            number specified is not an integer, the multimeter rounds it to an integer value.\n
            acal_code (str): Allows you to secure autocalibration. The choices are:\n
                - OFF (0) Disables autocal security; no code required for autocal\n
                - ON (1) Enables autocal security; the security code is required to perform autocal\n

        Remarks:
            - Specifying 0 for the new_code disables the security feature making it no longer
            necessary to enter the security code to perform a calibration or autocal.\n
            - The front panel's Last Entry key will not display the codes used in a previously
            executed SECURE command.\n

        Returns:
            bool: status
        """
        return self.__write_data(f'SECURE {old},{new},{acal_code}')
    
    def set_data_in_math_register(self, register, data) -> bool:
        """Places a number in a math register.

        Args:
            register (str): The register parameter choices are:\n
                - DEGREE (1) Time constant for FILTER and RMS\n
                - LOWER (2) Smallest reading in STATS\n
                - MAX (3) Upper Limit for PFAIL operation\n
                - MEAN (4) Average of readings in STATS\n
                - MIN (5) Lower limit for PFAIL\n
                - NSAMP (6) Number of samples in STATS\n
                - OFFSET (7) Subtrahend in NULL and SCALE operations\n
                - PERC (8) % value for PERC operation\n
                - REF (9) Reference value for DB operation\n
                - RES (10) Reference impedance for DBM operation\n
                - SCALE (11) Divisor in the SCALE operation\n
                - SDEV (12) Standard deviation in STATS\n
                - UPPER (13) Largest reading in STATS\n
                - HIRES (14) Not used by any math operation (extra register)\n
                - PFAILNUM (15) The number of reading that passed PFAIL before a failure was encountered\n
            
            data (float): The number parameter is the value to be placed in the register.
        
            Remarks:
                - You can use the SMATH command to place a number into one of the registers
                that store readings (UPPER, LOWER, etc.); however, that value will be replaced
                with a reading if the corresponding math function is enabled (e.g. STATS).\n
                - You cannot use -1 (minus 1) to default the number parameter. If you specify
                -1, you will actually write -1 to the register.\n

        Returns:
            bool: status
        """
        if register in ['DEGREE', 'LOWER', 'MAX', 'MEAN', 'MIN', 'NSAMP', 'OFFSET', 'PERC', 'REF', 'RES', 'SCALE', 'SDEV', 'UPPER', 'HIRES', 'PFAILNUM']:
            return self.__write_data(f'SMATH {register},{data}')
        else:
            return False
        
    def set_service_request(self) -> bool:
        """Sets bit 2 in the multimeter's status register. If bit 2 is enabled to
            assert SRQ (RQS 4 command), executing the SRQ command will set the GPIB
            SRQ line.

        Returns:
            bool: status
        """
        return self.__write_data(f'SRQ')
    
    def set_multimeter_state(self, name) -> bool:
        """Stores the multimeter's present state and assigns it a name. States
            are recalled using the RSTATE command.

        Args:
            name (str):State name. A state name may contain up to 10 characters. The name can be
            alpha, alphanumeric, or an integer in the range of 0 to 127. When using an
            alphanumeric name, the first character must be alpha. Alpha or alphanumeric
            state names must not be the same as multimeter commands or parameters or the
            name of a stored subprogram. The characters _ and ? can also be used in an alpha
            or alphanumeric name.
            When using an integer state name (0 - 127), the multimeter assigns the prefix
            STATE to the integer when the state is stored. This differentiates an integer state
            name from an integer subprogram name. For example, a state stored with the
            name 8 will be recorded as STATE8. The state can be recalled later using either
            the name 8 or STATE8. State 0 is reserved for the multimeter's power-down state
            (see first Remark below).
        
        Remarks:
            - Whenever the multimeter's power is removed, the present state is stored in
            state 0. After a power failure, the multimeter can be configured to its previous
            state by executing RSTATE 0.\n
            - All states are stored in continuous memory (not lost when power is removed).\n
            - Subprograms, the contents of reading memory, user-defined keys, and the
            front panel MENU mode are not included as part of a stored state. The
            contents of the following math registers are stored when you store a state (all
            other math registers are set to 0): DEGREE, LOWER, OFFSET, PERC, REF, RES, SCALE, and UPPER.\n
            - The multimeter has 14k-bytes of state memory. Each state occupies
            approximately 300 bytes allowing a maximum of 46 stored states. State 0 is
            reserved for storing the multimeter's state when power is removed. State 0
            may be also be used for storing other states, but the stored state will be
            overwritten with the present state when power is removed.\n
            - From the front panel, you can review the names of all stored states by pressing
            the Recall State key and using the up and down arrow keys. When you have
            found the desired state, press the Enter key to recall that state.\n

        Returns:
            bool: status
        """
        return self.__write_data(f'SSTATE {name}')
    
    def get_status_byte(self) -> str:
        """The status register contains seven bits that monitor various
            multimeter conditions. When a condition occurs, the corresponding bit is set in
            the status register. The STB? (status byte?) command returns a number
            representing the set bits. The returned number is the weighted sum of all set bits.
            The status register conditions and their weights are:\n
            -1 Subprogram Execution Completed\n
            -2 Hi or Lo Limit Exceeded\n
            -4 SRQ Command Executed\n
            -8 Power On\n
            -16 Ready for Instructions\n
            -32 Error (Consult Error Register)\n
            -64 Service Requested (you cannot disable this bit)\n
            -128 Data Available\n

        Remarks:
            - When you execute the STB? Command, the ready bit (bit 4) is always clear (not
            ready) because the multimeter is processing the STB? command.\n
            - The CSB command clears the status register (bits 4, 5, and 6 are not cleared if
            the condition(s) that set the bit(s) still exist). The RQS command designates
            which status register conditions will assert SRQ on the GPIB bus.\n

        Returns:
            str: status byte.
        """
        return self.__get_data(f'STB?')
    
    def set_start_of_subprogram(self, name) -> bool:
        """Stores a series of commands as a subprogram and assigns the
        sub-program name.

        Args:
            name (str):Subprogram name. A subprogram name may contain up to 10 characters. The
            name can be alpha, alphanumeric, or an integer from 0 to 127. When using an
            alphanumeric name, the first character must be alpha. Alpha or alphanumeric
            subprogram names must not be the same as multimeter commands or
            parameters or the name of a stored state. The characters _ and ? can also be
            included in an alpha or alphanumeric name.
            When using an integer subprogram name (0 - 127), the multimeter assigns the
            prefix SUB to the integer when the subprogram is stored. This differentiates an
            integer subprogram name from an integer state name. For example, a
            sub-program stored with the name 15 will be recorded as SUB15. The
            subprogram can be accessed later using either the name 15 or SUB15. A
            subprogram named 0 (zero) is designated the autostart subprogram (see 7th
            Remark following).\n

        Remarks:
            - Subprogram entry is terminated by the SUBEND command. The CALL
            command is used to execute a subprogram, and the PAUSE and CONT
            commands suspend and resume subprogram execution, respectively.\n
            - When you store a new subprogram using the name of an existing subprogram,
            the new subprogram overwrites (replaces) the old subprogram.\n
            - Entering (storing) a subprogram from the front panel is not recommended
            since front panel utilities (e.g., up and down arrows) can inadvertently be
            stored in the subprogram. Once you have executed the SUB command from
            the front panel, the display shows SUB ENTRY MODE until the SUBEND
            command is executed or the RESET key is pressed. The SUBEND command
            does not appear in the front panel menu unless you are storing a subprogram.\n
            - If a SCRATCH, DELSUB, a second SUB command, or the GPIB Device Clear
            command occurs in a subprogram, the multimeter does not store the
            command but does store the rest of the subprogram. Subprogram execution
            will be aborted if the RESET command is encountered (do not store RESET in a
            subprogram).\n
            - You can not store a subprogram with less than 800 bytes of subprogram/state
            memory remaining.\n
            - Subprogram execution will be aborted if an error is detected or the GPIB
            Device Clear command is received. The GPIB Device Clear command will also
            abort the process of storing a subprogram.\n
            - The only way to take readings within a subprogram is to use the TARM SGL or
            TRIG SGL command. When either of these commands is encountered, the
            multimeter will not execute the next command in the subprogram until all
            specified readings are taken. (This also means all configuration and other
            triggering commands must occur before the TARM SGL or TRIG SGL
            command.) Any other trigger arm or trigger events (except TARM EXT, see next
            Remark) will be executed in a subprogram, but the readings will not be
            initiated until the subprogram is complete.\n
            - Whenever the TARM EXT command is encountered in a subprogram, the
            multimeter waits until an external trigger is received on its Ext Trig connector
            before executing the next line of the subprogram. This allows you to
            synchronize subprogram execution to external equipment.\n
            - Any subprogram named 0 will be automatically executed whenever the
            multimeter has finished its power-on sequence. This is useful to recall the
            multimeter's previous state (RSTATE 0) following a power failure. \n
            - Subprograms are stored in continuous memory (not lost when power is
            removed). If you compress a subprogram, however, (COMPRESS command)
            the subprogram is removed from continuous memory and will be destroyed
            when power is removed.\n
            
        Returns:
            bool: status
        """ 
        return self.__write_data(f'SUB {name}')
    
    def set_end_of_subprogram(self) -> bool:
        """Signals the end of a subprogram.

        Remarks:
            - When storing a subprogram, SUBEND signals the end of the subprogram.
            When a subprogram has been executed, SUBEND sets bit 1 (if enabled) in the
            status register which signals the subprogram's completion.\n
        
        Returns:
            bool: status
        """
        return self.__write_data(f'SUBEND')
    
    def set_trigger_arm(self, event, number_arms=0) -> bool:
        """Defines the event that enables (arms) the trigger event (TRIG
            command). You can also use this command to perform multiple measurement
            cycles.
        Args:
            event (str): The event parameter choices are:\n
                AUTO (1) Always armed \n
                EXT (2) Arms following a low-going TTL transition on the Ext Trig
                connector. (Executing TARM EXT clears the trigger buffer if TBUFF is ON).\n
                SGL (3) Arms once (upon receipt of TARM SGL) then becomes HOLD\n
                HOLD (4) Triggering is disabled\n
                SYN (5) Arms when the multimeter's output buffer is empty, reading
                memory is off or empty, and the controller requests data.\n

            number_arms (int): The number_arms parameter is valid only with the SGL trigger arm event; in this
                case, the valid range is 0 - 2.1E+9. Specifying 0 or 1 with the SGL event has the
                same effect as using the default value (1): the trigger is armed once and then
                reverts to the HOLD state (disabled). When you specify a number greater than 1
                as the number_arms parameter, you have selected “multiple arming.” In multiple
                arming, the multimeter generates enough single trigger arms to satisfy the
                number_arms parameter. Refer to “multiple arming” in the Remarks section below
                for more information.\n 

        Remarks:
            - For all measurement functions except sub-sampling, the
            trigger arm event operates along with the trigger event (TRIG command) and
            the sample event (NRDGS or SWEEP command). To make a measurement, the
            trigger arm event must occur first, followed by the trigger event, and finally the
            sample event.\n
            - The trigger arm event does not necessarily trigger the multimeter. It merely
            enables the trigger event, making it possible for the multimeter to respond to the trigger event.\n
            - Multiple arming: When using multiple arming, the trigger arm event must be
            specified as SGL. When the multimeter executes a TARM command specifying
            multiple arming, it holds the GPIB bus until all measurement cycles are
            complete. For example, if you specify number_arms as 5, and 10 readings per
            cycle (NRDGS command), there are 5 measurement cycles of 10 readings
            each. Since it holds the bus, the TARM command must be the last line in the
            program and you cannot use the synchronous trigger event or sample event.\n

        Returns:
            bool: status
        """
        return self.__write_data(f'TARM {event},{number_arms}')
    
    def get_trigger_arm(self) -> str:
        """Returns the trigger arm setting.

        Returns:
            str: trigger arm setting.
        """
        return self.__get_data(f'TARM?')
    
    def set_ext_trigger_buffer_enabled(self, state) -> bool:
        """Enables or disables the multimeter's external trigger buffer.

        Args:
            state (str): The state parameter choices are:\n
                - OFF (0) Disables the trigger buffer which enables the TRIGGER TOO FAST error
                - ON (1) Enables and clears the trigger buffer which disables the TRIGGER TOO FAST error

        Remarks
            - Setting TBUFF to ON corrects for a TRIGGER TOO FAST error that can occur
            when using an external EXT trigger arm, trigger, or sample event. With TBUFF
            OFF, any external trigger occurring during a reading generates the TRIGGER
            TOO FAST error and the trigger(s) are ignored. With TBUFF ON, the first
            external trigger occurring during a reading is stored and no error is generated
            by this or any successive triggers. After the reading is complete, the stored
            trigger satisfies the EXT event if the multimeter is so programmed.\n
            - Executing the RESET command sets TBUFF to OFF.\n

        Returns:
            bool: status
        """
        return self.__write_data(f'TBUFF {state}')
    
    def get_ext_trigger_buffer_enabled(self) -> str:
        """Returns the external trigger buffer setting.

        Returns:
            str: external trigger buffer setting.
        """
        return self.__get_data(f'TBUFF?')
    
    def get_internal_temperature(self) -> str:
        """Returns the multimeter's internal temperature in degrees Centigrade.\n

        Remarks:
            - Monitoring the multimeter's temperature is helpful to determine when to
            perform autocalibration.\n
        
        Returns:
            str: internal temperature.
        """
        return self.__get_data(f'TEMP?')
    
    def self_test(self) -> str:
        """Causes the multimeter to perform a series of internal self-tests.

        Remarks:
            - Always disconnect any input signals before you run self-test. If you leave an
            input signal connected to the multimeter, it may cause a self-test failure.\n
            - If a hardware error is detected, the multimeter sets bit 0 in the error register
            and a more descriptive bit in the auxiliary error register. The display's ERR
            annunciator illuminates whenever an error register bit is set. You can access
            the error registers using ERRSTR? (both registers), ERR? (error register only),
            or AUXERR? (auxiliary error register only).\n

        Returns:
            str: self-test result.
        """
        return self.__get_data(f'TEST')
    
    def beep(self) -> bool:
        """Causes the multimeter to beep once. The multimeter then returns to the previous
            BEEP mode (either OFF or ON).

        Returns:
            bool: status
        """
        return self.__write_data(f'BEEP')
    
    def set_trigger_event(self, event) -> bool:
        """Defines the event that initiates a measurement. The trigger event
            operates along with the trigger arm event (TARM command) and the sample event
            (NRDGS or SWEEP command). To make a measurement, the trigger arm event must
            occur first, followed by the trigger event, and finally the sample event.

        Args:
            event (str): The event parameter choices are:\n
                - AUTO (1) Always triggers\n
                - EXT (2) Triggers on a low-going TTL transition on the Ext Trig connector\n
                - SGL (3) Triggers once (upon receipt of TRIG SGL) then becomes HOLD\n
                - HOLD (4) Triggering is disabled\n
                - SYN (5) Triggers when the multimeter's output buffer is empty, reading memory
                is off or empty, and the controller requests data\n
                - LEVEL (7) Triggers when the input signal reaches the voltage specified by the
                LEVEL command on the slope specified by the SLOPE command. Can be used with only for 
                DC voltage and direct-sampled measurements\n
                - TRIG (8) Triggers on a zero crossing of the AC line voltage. Cannot be used for
                sampled AC or AC+DC voltage measurements (SETACV RDDM or SYNC) or for frequency or
                period measurements.\n

        Remarks
            - For all measurements except sub-sampling (see Chapter 5), the trigger event
            operates along with the trigger arm event (TARM command) and the sample
            event (NRDGS command). (The trigger event and the sample event are ignored
            for sub-sampling.) To make a measurement, the trigger arm event must occur
            first, followed by the trigger event, and finally the sample event. The trigger
            event does not initiate a measurement. It merely enables a measurement,
            making it possible for a measurement to take place. The measurement is
            initiated when the sample event (NRDGS or SWEEP command) occurs. Refer
            to Triggering Measurements in Chapter 4 for an in-depth discussion of the
            interaction of the various events for most measurement functions. Refer to
            Chapter 5 for information on sub-sampling.\n
                
        Returns:
            bool: status
        """
        
        if event in ['AUTO', 'EXT', 'SGL', 'HOLD', 'SYN', 'LEVEL', 'TRIG']:
            return self.__write_data(f'TRIG {event}')
        else:
            return False
        
    def get_trigger_event(self) -> str:
        """Returns the trigger event setting.

        Returns:
            str: trigger event setting.
        """
        return self.__get_data(f'TRIG?')
    
    def set_volate_dc_function(self)-> bool:
        """Sets function to DCV

        Returns:
            bool: status
        """
        return self.__write_data('FUNC DCV')

    def set_voltage_dc_rang_res(self, max_input=1000, perc_resolution=0) -> bool:
        """Selects DC voltage measurements.

        Args:
            max_input (float): Selects a fixed range or the autorange mode. To select a fixed range, you specify
            max_input as the absolute value (no negative numbers) of the input signal's
            maximum expected amplitude. The multimeter then selects the correct range.
            To select autorange, specify AUTO for max._input or default the parameter. In the
            autorange mode, the multimeter samples the input signal before each reading
            and selects the appropriate range. Possible values are:\n
                - -1 or AUTO: autorange\n
                - from 0 to 0.12 range 100 mV full scale 120 mV\n
                - from 0.12 to 1.2 range 1 V full scale 1.2 V\n
                - from 1.2 to 12 range 10 V full scale 12 V\n
                - from 12 to 120 range 100 V full scale 120 V\n
                - from 120 to 1E3 range 1000 V full scale 1050 V\n


            perc_resolution (float): Specify the %_resolution as a percentage of
            the max._input parameter. To determine %_resolution, use the equation:
            %_resolution = (actual resolution/maximum input) * 100
            
        Returns:
            bool: status
        """
        if (max_input == 'AUTO' or max_input == -1 or (max_input >= 0 and max_input <= 1050)) and perc_resolution >= 0:
            return self.__write_data(f'DCV {max_input},{perc_resolution}')
        else:
            return False
        
    def set_voltage_ac_function(self) -> bool:
        """Sets function to ACV

        Returns:
            bool: status
        """
        return self.__write_data('FUNC ACV')
    
    def set_voltage_ac_rang_res(self, max_input=1000, perc_resolution=0) -> bool:
        """Selects AC voltage measurements.

        Args:
            max_input (float): Selects a fixed range or the autorange mode. To select a fixed range, you specify
            max_input as the absolute value (no negative numbers) of the input signal's
            maximum expected amplitude. The multimeter then selects the correct range.
            To select autorange, specify AUTO for max._input or default the parameter. In the
            autorange mode, the multimeter samples the input signal before each reading
            and selects the appropriate range. Possible values are:\n
                - -1 or AUTO: autorange\n
                - from 0 to 0.012 range 10 mV full scale 12 mV\n
                - from 0.012 to 0.12 range 100 mV full scale 120 mV\n
                - from 0.12 to 1.2 range 1 V full scale 1.2 V\n
                - from 1.2 to 12 range 10 V full scale 12 V\n
                - from 12 to 120 range 100 V full scale 120 V\n
                - from 120 to 1E3 range 1000 V full scale 1050 V\n


            perc_resolution (float): Specify the %_resolution as a percentage of
            the max._input parameter. To determine %_resolution, use the equation:
            %_resolution = (actual resolution/maximum input) * 100
            
        Returns:
            bool: status
        """
        if (max_input == 'AUTO' or max_input == -1 or (max_input >= 0 and max_input <= 1050)) and perc_resolution >= 0:
            return self.__write_data(f'ACV {max_input},{perc_resolution}')
        else:
            return False
        
    def set_voltage_acdcv_function(self) -> bool:
        """Sets function to ACDCV

        Returns:
            bool: status
        """
        return self.__write_data('FUNC ACDCV')
    
    def set_voltage_acdcv_rang_res(self, max_input=1000, perc_resolution=0) -> bool:
        """Selects AC voltage measurements.

        Args:
            max_input (float): Selects a fixed range or the autorange mode. To select a fixed range, you specify
            max_input as the absolute value (no negative numbers) of the input signal's
            maximum expected amplitude. The multimeter then selects the correct range.
            To select autorange, specify AUTO for max._input or default the parameter. In the
            autorange mode, the multimeter samples the input signal before each reading
            and selects the appropriate range. Possible values are:\n
                - -1 or AUTO: autorange\n
                - from 0 to 0.012 range 10 mV full scale 12 mV\n
                - from 0.012 to 0.12 range 100 mV full scale 120 mV\n
                - from 0.12 to 1.2 range 1 V full scale 1.2 V\n
                - from 1.2 to 12 range 10 V full scale 12 V\n
                - from 12 to 120 range 100 V full scale 120 V\n
                - from 120 to 1E3 range 1000 V full scale 1050 V\n


            perc_resolution (float): Specify the %_resolution as a percentage of
            the max._input parameter. To determine %_resolution, use the equation:
            %_resolution = (actual resolution/maximum input) * 100
            
        Returns:
            bool: status
        """
        if (max_input == 'AUTO' or max_input == -1 or (max_input >= 0 and max_input <= 1050)) and perc_resolution >= 0:
            return self.__write_data(f'ACDCV {max_input},{perc_resolution}')
        else:
            return False
        
    def set_current_dc_function(self) -> bool:
        """Sets function to DCI

        Returns:
            bool: status
        """
        return self.__write_data('FUNC DCI')
    
    def set_current_dc_rang_res(self, max_input=1, perc_resolution=0) -> bool:
        """Selects DC current measurements.

        Args:
            max_input (float): Selects a fixed range or the autorange mode. To select a fixed range, you specify
            max_input as the absolute value (no negative numbers) of the input signal's
            maximum expected amplitude. The multimeter then selects the correct range.
            To select autorange, specify AUTO for max._input or default the parameter. In the
            autorange mode, the multimeter samples the input signal before each reading
            and selects the appropriate range. Possible values are:\n
                - -1 or AUTO: autorange\n
                - from 0 to 0.12E-6 range 100 nA full scale 120 nA\n
                - from 0.12E-6 to 1.2E-6 range 1 μA full scale 1.2 μA\n
                - from 1.2E-6 to 12E-6 range 10 μA full scale 12 μA\n
                - from 12E-6 to 120E-6 range 100 μA full scale 120 μA\n
                - from 120E-6 to 1.2E-3 range 1 mA full scale 1.2 mA\n
                - from 1.2E-3 to 12E-3 range 10 mA full scale 12 mA\n
                - from 12E-3 to 120E-3 range 100 mA full scale 120 mA\n
                - from 120E-3 to 1.2 range 1 A full scale 1.05 A\n

            perc_resolution (float): Specify the %_resolution as a percentage of
            the max._input parameter. To determine %_resolution, use the equation:
            %_resolution = (actual resolution/maximum input) * 100
            
        Returns:
            bool: status
        """
        if (max_input == 'AUTO' or max_input == -1 or (max_input >= 0 and max_input <= 1.2)) and perc_resolution >= 0:
            return self.__write_data(f'DCI {max_input},{perc_resolution}')
        else:
            return False
        
    def set_current_ac_function(self) -> bool:
        """Sets function to ACI

        Returns:
            bool: status
        """
        return self.__write_data('FUNC ACI')
    
    def set_current_ac_rang_res(self, max_input=1, perc_resolution=0) -> bool:
        """Selects AC current measurements.

        Args:
            max_input (float): Selects a fixed range or the autorange mode. To select a fixed range, you specify
            max_input as the absolute value (no negative numbers) of the input signal's
            maximum expected amplitude. The multimeter then selects the correct range.
            To select autorange, specify AUTO for max._input or default the parameter. In the
            autorange mode, the multimeter samples the input signal before each reading
            and selects the appropriate range. Possible values are:\n
                - -1 or AUTO: autorange\n
                - from 12E-6 to 120E-6 range 100 μA full scale 120 μA\n
                - from 120E-6 to 1.2E-3 range 1 mA full scale 1.2 mA\n
                - from 1.2E-3 to 12E-3 range 10 mA full scale 12 mA\n
                - from 12E-3 to 120E-3 range 100 mA full scale 120 mA\n
                - from 120E-3 to 1.2 range 1 A full scale 1.05 A\n

            perc_resolution (float): Specify the %_resolution as a percentage of
            the max._input parameter. To determine %_resolution, use the equation:
            %_resolution = (actual resolution/maximum input) * 100
            
        Returns:
            bool: status
        """
        if (max_input == 'AUTO' or max_input == -1 or (max_input >= 0 and max_input <= 1.2)) and perc_resolution >= 0:
            return self.__write_data(f'ACI {max_input},{perc_resolution}')
        else:
            return False
        
    def set_current_acdci_function(self) -> bool:
        """Sets function to ACDCI

        Returns:
            bool: status
        """
        return self.__write_data('FUNC ACDCI')
    
    def set_current_acdci_rang_res(self, max_input=1, perc_resolution=0) -> bool:
        """Selects ACDCI current measurements.

        Args:
            max_input (float): Selects a fixed range or the autorange mode. To select a fixed range, you specify
            max_input as the absolute value (no negative numbers) of the input signal's
            maximum expected amplitude. The multimeter then selects the correct range.
            To select autorange, specify AUTO for max._input or default the parameter. In the
            autorange mode, the multimeter samples the input signal before each reading
            and selects the appropriate range. Possible values are:\n
                - -1 or AUTO: autorange\n
                - from 12E-6 to 120E-6 range 100 μA full scale 120 μA\n
                - from 120E-6 to 1.2E-3 range 1 mA full scale 1.2 mA\n
                - from 1.2E-3 to 12E-3 range 10 mA full scale 12 mA\n
                - from 12E-3 to 120E-3 range 100 mA full scale 120 mA\n
                - from 120E-3 to 1.2 range 1 A full scale 1.05 A\n

            perc_resolution (float): Specify the %_resolution as a percentage of
            the max._input parameter. To determine %_resolution, use the equation:
            %_resolution = (actual resolution/maximum input) * 100
            
        Returns:
            bool: status
        """
        if (max_input == 'AUTO' or max_input == -1 or (max_input >= 0 and max_input <= 1.2)) and perc_resolution >= 0:
            return self.__write_data(f'ACDCI {max_input},{perc_resolution}')
        else:
            return False
        
    def set_ohm_function(self) -> bool:
        """Selects 2-wire ohms measurements

        Returns:
            bool: status
        """
        return self.__write_data('FUNC OHM')
    
    def set_ohm_rang_res(self, max_input=1, perc_resolution=0) -> bool:
        """Selects 2-wire ohms measurements.

        Args:
            max_input (float): Selects a fixed range or the autorange mode. To select a fixed range, you specify
            max_input as the absolute value (no negative numbers) of the maximum resistance for ohms
            measurements. The multimeter then selects the correct range.
            To select autorange, specify AUTO for max._input or default the parameter. In the
            autorange mode, the multimeter samples the input signal before each reading
            and selects the appropriate range. Possible values are:\n
                - -1 or AUTO: autorange\n
                - from 0 to 12 range 10 Ω full scale 12 Ω\n
                - from 12 to 120 range 100 Ω full scale 120 Ω\n
                - from 120 to 1E3 range 1 kΩ full scale 1.2 kΩ\n
                - from 1E3 to 12 range 10 kΩ full scale 12 kΩ\n
                - from 12 to 120 range 100 kΩ full scale 120 kΩ\n
                - from 120 to 1E6 range 1 MΩ full scale 1.2 MΩ\n
                - from 1E6 to 12 range 10 MΩ full scale 12 MΩ\n
                - from 12 to 120 range 100 MΩ full scale 120 MΩ\n
                - from 120 to 1E9 range 1 GΩ full scale 1.2 GΩ\n

            perc_resolution (float): Specify the %_resolution as a percentage of
            the max._input parameter. To determine %_resolution, use the equation:
            %_resolution = (actual resolution/maximum input) * 100
            
        Returns:
            bool: status
        """
        if (max_input == 'AUTO' or max_input == -1 or (max_input >= 0 and max_input <= 1E9)) and perc_resolution >= 0:
            return self.__write_data(f'OHM {max_input},{perc_resolution}')
        else:
            return False
        
    def set_4_wire_ohm_function(self) -> bool:
        """Selects 4-wire ohms measurements

        Returns:
            bool: status
        """
        return self.__write_data('FUNC OHMF')
    
    def set_4_wire_rang_res(self, max_input=1, perc_resolution=0) -> bool:
        """Selects 4-wire ohms measurements.

        Args:
            max_input (float): Selects a fixed range or the autorange mode. To select a fixed range, you specify
            max_input as the absolute value (no negative numbers) of the maximum resistance for ohms
            measurements. The multimeter then selects the correct range.
            To select autorange, specify AUTO for max._input or default the parameter. In the
            autorange mode, the multimeter samples the input signal before each reading
            and selects the appropriate range. Possible values are:\n
                - -1 or AUTO: autorange\n
                - from 0 to 12 range 10 Ω full scale 12 Ω\n
                - from 12 to 120 range 100 Ω full scale 120 Ω\n
                - from 120 to 1E3 range 1 kΩ full scale 1.2 kΩ\n
                - from 1E3 to 12 range 10 kΩ full scale 12 kΩ\n
                - from 12 to 120 range 100 kΩ full scale 120 kΩ\n
                - from 120 to 1E6 range 1 MΩ full scale 1.2 MΩ\n
                - from 1E6 to 12 range 10 MΩ full scale 12 MΩ\n
                - from 12 to 120 range 100 MΩ full scale 120 MΩ\n
                - from 120 to 1E9 range 1 GΩ full scale 1.2 GΩ\n

            perc_resolution (float): Specify the %_resolution as a percentage of
            the max._input parameter. To determine %_resolution, use the equation:
            %_resolution = (actual resolution/maximum input) * 100
            
        Returns:
            bool: status
        """
        if (max_input == 'AUTO' or max_input == -1 or (max_input >= 0 and max_input <= 1E9)) and perc_resolution >= 0:
            return self.__write_data(f'OHMF {max_input},{perc_resolution}')
        else:
            return False
        
    def set_dsac_function(self) -> bool:
        """Configures the multimeter for direct-sampled measurements
        (digitizing). The DSAC function measures only the AC component of the input
        waveform.

        Returns:
            bool: status
        """
        return self.__write_data('FUNC DSAC')
    
    def set_dsac_rang(self, max_input=1) -> bool:
        """Configures the multimeter for direct-sampled measurements
        (digitizing). The DSAC function measures only the AC component of the input
        waveform.The DSAC functions use the
        track/hold circuit (2 nanosecond aperture) and a wide bandwidth input path
        (12 MHz bandwidth).

        Args:
            max_input (float): Selects the measurement range. (You cannot use autorange for direct-sampled
            measurements). To select a range, you specify max._input as the input signal's
            expected peak amplitude. The multimeter then selects the correct range. The
            following table shows the max._input parameters and the ranges they select.
            Possible values are:\n
                - from 0 to 0.012 range 10 mV full scale SINT format 12 mV DINT format 50 mV \n
                - from 0.012 to 0.12 range 100 mV full scale SINT format 120 mV DINT format 500 mV \n
                - from 0.12 to 1.2 range 1 V full scale SINT format 1.2 V DINT format 5 V \n
                - from 1.2 to 12 range 10 V full scale SINT format 12 V DINT format 50 V \n
                - from 12 to 120 range 100 V full scale SINT format 120 V DINT format 500 V \n
                - from 120 to 1E3 range 1000 V full scale SINT format 1050 V DINT format 1050 V \n

        Remarks:
            - You cannot use autorange for direct-sampled measurements: you must specify
            the range as the first parameter of the DSAC or DSDC command (max._input
            parameter).\n
            - Notice that when using the DINT memory/output format the full scale values
            for direct-sampling are 500% (5 times) the ranges of 10 mV, 100 mV, 1 V, 10 V,
            and 100 V. This is particularly important to consider when specifying the
            percentage for level triggering. When specifying the level triggering voltage,
            use a percentage of the range. For example, assume the input signal has a
            peak value of 20 V and you are using the 10 V range. If you want to level
            trigger at 15 V, specify a level triggering percentage of 150% (LEVEL 150
            command). (The slew rate of the multimeter's amplifiers may be exceeded
            when measuring a signal with a frequency >2 MHz and an amplitude >120% of
            range; signals <120% of range with frequencies up to 12 MHz do not cause
            slew rate errors.)\n
            - The multimeter's triggering hierarchy (trigger arm event, trigger event, and
            sample event) applies to direct-sampling. This means that these events must
            occur in the proper order before direct-sampling begins. Refer to Chapter 4 for
            more information on the triggering hierarchy. For direct-sampling, you can use
            either the TlMER sample event and the NRDGS n,TIMER command, or the
            SWEEP command (SWEEP is the simpler to program). The NRDGS and
            SWEEP commands are interchangeable, the multimeter uses whichever
            command was specified last. (When using the SWEEP command, the sample
            event is automatically set to TIMER.)\n
            - For direct-sampling, you should use the SINT memory/output format when the
            peak value of the input signal is <120% of the specified range. Use the DINT
            memory/output format when the input signal is ≥120% of the range. (SINT and
            DINT are the formats used internally by the A/D converter; by using the correct
            memory/output format, no format conversions are necessary.)\n
            
        Returns:
            bool: status
        """
        if max_input >= 0 and max_input <= 1E3:
            return self.__write_data(f'DSAC {max_input}')
        else:
            return False
        

    def set_dsdc_function(self) -> bool:
        """Configures the multimeter for direct-sampled measurements
        (digitizing). The DSDC function measures the combined AC and DC components.

        Returns:
            bool: status
        """
        return self.__write_data('FUNC DSDC')
    
    def set_dsdc_rang(self, max_input=1) -> bool:
        """Configures the multimeter for direct-sampled measurements
        (digitizing). The DSDC function measures the combined AC and DC components.
        Otherwise, the two functions are identical. The DSDC functions use the
        track/hold circuit (2 nanosecond aperture) and a wide bandwidth input path
        (12 MHz bandwidth).

        Args:
            max_input (float): Selects the measurement range. (You cannot use autorange for direct-sampled
            measurements). To select a range, you specify max._input as the input signal's
            expected peak amplitude. The multimeter then selects the correct range. The
            following table shows the max._input parameters and the ranges they select.
            Possible values are:\n
                - from 0 to 0.012 range 10 mV full scale SINT format 12 mV DINT format 50 mV \n
                - from 0.012 to 0.12 range 100 mV full scale SINT format 120 mV DINT format 500 mV \n
                - from 0.12 to 1.2 range 1 V full scale SINT format 1.2 V DINT format 5 V \n
                - from 1.2 to 12 range 10 V full scale SINT format 12 V DINT format 50 V \n
                - from 12 to 120 range 100 V full scale SINT format 120 V DINT format 500 V \n
                - from 120 to 1E3 range 1000 V full scale SINT format 1050 V DINT format 1050 V \n

        Remarks:
            - You cannot use autorange for direct-sampled measurements: you must specify
            the range as the first parameter of the DSAC or DSDC command (max._input
            parameter).\n
            - Notice that when using the DINT memory/output format the full scale values
            for direct-sampling are 500% (5 times) the ranges of 10 mV, 100 mV, 1 V, 10 V,
            and 100 V. This is particularly important to consider when specifying the
            percentage for level triggering. When specifying the level triggering voltage,
            use a percentage of the range. For example, assume the input signal has a
            peak value of 20 V and you are using the 10 V range. If you want to level
            trigger at 15 V, specify a level triggering percentage of 150% (LEVEL 150
            command). (The slew rate of the multimeter's amplifiers may be exceeded
            when measuring a signal with a frequency >2 MHz and an amplitude >120% of
            range; signals <120% of range with frequencies up to 12 MHz do not cause
            slew rate errors.)\n
            - The multimeter's triggering hierarchy (trigger arm event, trigger event, and
            sample event) applies to direct-sampling. This means that these events must
            occur in the proper order before direct-sampling begins. Refer to Chapter 4 for
            more information on the triggering hierarchy. For direct-sampling, you can use
            either the TlMER sample event and the NRDGS n,TIMER command, or the
            SWEEP command (SWEEP is the simpler to program). The NRDGS and
            SWEEP commands are interchangeable, the multimeter uses whichever
            command was specified last. (When using the SWEEP command, the sample
            event is automatically set to TIMER.)\n
            - For direct-sampling, you should use the SINT memory/output format when the
            peak value of the input signal is <120% of the specified range. Use the DINT
            memory/output format when the input signal is ≥120% of the range. (SINT and
            DINT are the formats used internally by the A/D converter; by using the correct
            memory/output format, no format conversions are necessary.)\n
            
        Returns:
            bool: status
        """
        if max_input >= 0 and max_input <= 1E3:
            return self.__write_data(f'DSDC {max_input}')
        else:
            return False
        
    def set_frequency_function(self) -> bool:
        """Instructs the multimeter to measure the frequency of the input signal.
        You must specify whether the input signal is AC voltage, AC+DC voltage, AC
        current, or AC+DC current using the FSOURCE command.

        Returns:
            bool: status
        """
        return self.__write_data('FUNC FREQ')
    
    def set_frequency_rang_res(self, max_input=1, perc_resolution=0) -> bool:
        """Instructs the multimeter to measure the frequency of the input signal.
            You must specify whether the input signal is AC voltage, AC+DC voltage, AC
            current, or AC+DC current using the FSOURCE command.

        Args:
            max_input (float): Selects a fixed range or the autorange mode. The ranges correspond to the type
            of input signal specified in the FSOURCE command. That is, if ACV is the specified
            input signal, the max._input parameter specifies an AC voltage measurement
            range. To select a fixed range, you specify max._input as the absolute value (no
            negative numbers) of the expected peak value of the input signal. The multimeter
            then selects the proper range. Refer to the FUNC or RANGE command for tables
            showing the ranges available for each type of input signal.
            To select the autorange mode, specify AUTO for max._input or default the
            parameter. In the autorange mode, the multimeter samples the input signal
            before each frequency reading and selects the proper range.\n

            perc_resolution (float): The %_resolution parameter specifies the digits of resolution and the gate time as
            shown below:\n
            for perc_res .00001 gate time is 1 s and digit resolution is 7\n
            for perc_res .0001 gate time is 0.1 s and digit resolution is 7\n
            for perc_res .001 gate time is 0.01 s and digit resolution is 6\n
            for perc_res .01 gate time is 0.001 s and digit resolution is 5\n
            for perc_res .1 gate time is 0.0001 s and digit resolution is 4\n
        
        Remarks:
            - The reading rate is the longer of 1 period of the input signal, the gate time, or
            the default reading timeout of 1.2 seconds.\n
            - Frequency (and period) measurements are made using the level detection
            circuitry to determine when the input signal crosses a particular voltage on its
            positive or negative slope. (This is why you cannot use the LEVEL trigger or
            sample event or the LINE trigger event when making frequency or period
            measurements.) The power-on or default level triggering values select zero
            volts, positive slope. You can control the level triggering voltage and coupling
            using the LEVEL command. You can specify either the positive or negative
            slope using the SLOPE command.\n
            - The leftmost digit which is a half digit for most measurement functions, is a full
            digit (0 - 9) for frequency measurements.\n
            - Readings made with autorange enabled take longer because the input signal
            is sampled (to determine the proper range) between frequency readings.\n
            - For frequency (and period) measurements, an overload indication means the
            voltage or current amplitude is too great for the specified measurement range.
            It does not mean the applied frequency (or period) is too great to be measured.\n
            
        Returns:
            bool: status
        """
        if (max_input == 'AUTO' or max_input == -1 or max_input >= 0) and (perc_resolution >= 0 and perc_resolution<=0.1):
            return self.__write_data(f'FREQ {max_input},{perc_resolution}')
        else:
            return False
        

    def set_period_function(self) -> bool:
            """Instructs the multimeter to measure the period of the input signal. You can
            specify whether the input signal is AC voltage (default), AC+DC voltage, AC
            current, or AC+DC current using the FSOURCE command.

            Returns:
                bool: status
            """
            return self.__write_data('FUNC PER')
    
    def set_period_rang_res(self, max_input=1, perc_resolution=0) -> bool:
        """Instructs the multimeter to measure the period of the input signal. You can
            specify whether the input signal is AC voltage (default), AC+DC voltage, AC
            current, or AC+DC current using the FSOURCE command.

        Args:
            max_input (float): The max_input parameter selects a fixed range or the autorange mode. The
            ranges correspond to the type of input signal specified in the FSOURCE
            command. That is, if ACV is the specified input signal, the max._input parameter
            specifies an AC voltage measurement range. To select a fixed range, you specify
            max._input as the absolute value (no negative numbers) of the expected peak
            value of the input signal. The multimeter then selects the proper range. Refer to
            the FUNC or RANGE command for tables showing the ranges available for each
            type of input signal.
            To select the autorange mode, specify AUTO for max._input or default the
            parameter. In the autorange mode, the multimeter samples the input signal
            before each period reading and selects the proper range.\n

            perc_resolution (float): The %_resolution parameter specifies the digits of resolution and the gate time as
            shown below:\n
            for perc_res .00001 gate time is 1 s and digit resolution is 7\n
            for perc_res .0001 gate time is 0.1 s and digit resolution is 7\n
            for perc_res .001 gate time is 0.01 s and digit resolution is 6\n
            for perc_res .01 gate time is 0.001 s and digit resolution is 5\n
            for perc_res .1 gate time is 0.0001 s and digit resolution is 4\n
        
        Remarks:
            - The reading rate is the longer of 1 period of the input signal, the gate time, or
            the default reading timeout of 1.2 seconds.\n
            - Period measurements are made using the level detection
            circuitry to determine when the input signal crosses a particular voltage on its
            positive or negative slope. (This is why you cannot use the LEVEL trigger or
            sample event or the LINE trigger event when making period
            measurements.) The power-on or default level triggering values select zero
            volts, positive slope. You can control the level triggering voltage and coupling
            using the LEVEL command. You can specify either the positive or negative
            slope using the SLOPE command.\n
            - The leftmost digit which is a half digit for most measurement functions, is a full
            digit (0 - 9) for frequency measurements.\n
            - Readings made with autorange enabled take longer because the input signal
            is sampled (to determine the proper range) between frequency readings.\n
            - For period measurements, an overload indication means the
            voltage or current amplitude is too great for the specified measurement range.
            It does not mean the applied period is too great to be measured.\n
            
        Returns:
            bool: status
        """
        if (max_input == 'AUTO' or max_input == -1 or max_input >= 0) and (perc_resolution >= 0 and perc_resolution<=0.1):
            return self.__write_data(f'PER {max_input},{perc_resolution}')
        else:
            return False
        
    def set_ssac_function(self) -> bool:
        """Configures the multimeter for sub-sampled voltage
        measurements (digitizing). The SSAC function measures only the AC component
        of the input waveform. The SSDC function measures the combined AC and DC
        components of the waveform. Otherwise, the two functions are identical.

        Returns:
            bool: status
        """
        return self.__write_data('FUNC SSAC')
    
    def set_ssac_rang(self, max_input=1) -> bool:
        """Configures the multimeter for sub-sampled voltage
        measurements (digitizing). The SSAC function measures only the AC component
        of the input waveform. The SSDC function measures the combined AC and DC
        components of the waveform. Otherwise, the two functions are identical. The
        input signal must be periodic (repetitive) for sub-sampled measurements.
        Sub-sampled measurements use the track/hold circuit (2 nanoseconds aperture)
        and a wide bandwidth input. path (12 MHz bandwidth).

        Args:
            max_input (float): Selects the measurement range (you cannot use autorange for sub-sampled
            measurements). To select a range, you specify max._input as the input signal's
            expected peak amplitude. The multimeter then selects the correct range. The
            following table shows the max._input parameters and the ranges they select.
            Possible values are:\n
                - from 0 to 0.012 range 10 mV full scale 12 mV\n
                - from 0.012 to 0.12 range 100 mV full scale 120 mV\n
                - from 0.12 to 1.2 range 1 V full scale 1.2 V\n
                - from 1.2 to 12 range 10 V full scale 12 V\n
                - from 12 to 120 range 100 V full scale 120 V\n
                - from 120 to 1E3 range 1000 V full scale 1050 V\n

        Remarks:
            - Autozero and autorange do not function for sub-sampled measurements.
            Executing the SSAC or SSDC command suspends autozero and autorange
            operation.\n
            - As with direct-sampling, you can specify a level triggering voltage up to 500%
            of the range. The required SINT format, however, cannot handle samples
            greater then 120% of range.\n
            -If reading memory is disabled when you execute the SSAC or SSDC command,
            the multimeter automatically sets the output format to SINT (the memory
            format is not changed). Later, where you change to another measurement
            function, the output format returns to that previously specified. You must use
            the SINT output format when sub-sampling and outputting samples directly to
            the GPIB. You can, however, use any output format if the samples are first
            placed in reading memory (see next Remark). To do this, you should enable
            reading memory before executing the SSAC or SSDC command (executing
            SSAC or SSDC does not change the output format to SINT when reading
            memory is enabled).\n
            - When sub-sampling with reading memory enabled, reading memory must be
            in FIFO mode, must be empty (executing MEM FIFO clears reading memory),
            and the memory format must be SINT prior to the occurrence of the trigger
            arm event. If not, the multimeter generates the SETTINGS CONFLICT error
            when the trigger arm event occurs and no samples are taken.\n
            - For sub-sampling, the trigger event and the sample event are ignored. 
            The only triggering events that apply to sub-sampling are the trigger 
            arm event (TARM command) and the sync source event.\n
            - In sub-sampling, samples are taken on more than one period of the input
            waveform. When the samples are sent directly to reading memory (MEM
            command), the multimeter automatically reconstructs the samples producing
            a composite waveform. When the samples are sent to the output buffer, the
            controller must use an algorithm to reconstruct the composite waveform.
            parameters for this algorithm are provided by the SSPARM? command.\n
            - The effective_interval between samples and the total number of samples taken
            are specified by the SWEEP command. (You cannot use the NRDGS command
            for sub-sampling.) In sub-sampling, the multimeter will use as many periods of
            the input signal as necessary to achieve the specified effective_interval. The
            minimum effective_interval for sub-sampling is 10 nanoseconds.\n
            
        Returns:
            bool: status
        """
        if max_input >= 0 and max_input <= 1E3:
            return self.__write_data(f'SSAC {max_input}')
        else:
            return False
        

    def set_ssdc_function(self) -> bool:
        """Configures the multimeter for sub-sampled voltage
        measurements (digitizing). The SSAC function measures only the AC component
        of the input waveform. The SSDC function measures the combined AC and DC
        components of the waveform. Otherwise, the two functions are identical.

        Returns:
            bool: status
        """
        return self.__write_data('FUNC SSDC')
    
    def set_ssdc_rang(self, max_input=1) -> bool:
        """Configures the multimeter for sub-sampled voltage
        measurements (digitizing). The SSAC function measures only the AC component
        of the input waveform. The SSDC function measures the combined AC and DC
        components of the waveform. Otherwise, the two functions are identical. The
        input signal must be periodic (repetitive) for sub-sampled measurements.
        Sub-sampled measurements use the track/hold circuit (2 nanoseconds aperture)
        and a wide bandwidth input. path (12 MHz bandwidth).

        Args:
            max_input (float): Selects the measurement range (you cannot use autorange for sub-sampled
            measurements). To select a range, you specify max._input as the input signal's
            expected peak amplitude. The multimeter then selects the correct range. The
            following table shows the max._input parameters and the ranges they select.
            Possible values are:\n
                - from 0 to 0.012 range 10 mV full scale 12 mV\n
                - from 0.012 to 0.12 range 100 mV full scale 120 mV\n
                - from 0.12 to 1.2 range 1 V full scale 1.2 V\n
                - from 1.2 to 12 range 10 V full scale 12 V\n
                - from 12 to 120 range 100 V full scale 120 V\n
                - from 120 to 1E3 range 1000 V full scale 1050 V\n

        Remarks:
            - Autozero and autorange do not function for sub-sampled measurements.
            Executing the SSAC or SSDC command suspends autozero and autorange
            operation.\n
            - As with direct-sampling, you can specify a level triggering voltage up to 500%
            of the range. The required SINT format, however, cannot handle samples
            greater then 120% of range.\n
            -If reading memory is disabled when you execute the SSAC or SSDC command,
            the multimeter automatically sets the output format to SINT (the memory
            format is not changed). Later, where you change to another measurement
            function, the output format returns to that previously specified. You must use
            the SINT output format when sub-sampling and outputting samples directly to
            the GPIB. You can, however, use any output format if the samples are first
            placed in reading memory (see next Remark). To do this, you should enable
            reading memory before executing the SSAC or SSDC command (executing
            SSAC or SSDC does not change the output format to SINT when reading
            memory is enabled).\n
            - When sub-sampling with reading memory enabled, reading memory must be
            in FIFO mode, must be empty (executing MEM FIFO clears reading memory),
            and the memory format must be SINT prior to the occurrence of the trigger
            arm event. If not, the multimeter generates the SETTINGS CONFLICT error
            when the trigger arm event occurs and no samples are taken.\n
            - For sub-sampling, the trigger event and the sample event are ignored. 
            The only triggering events that apply to sub-sampling are the trigger 
            arm event (TARM command) and the sync source event.\n
            - In sub-sampling, samples are taken on more than one period of the input
            waveform. When the samples are sent directly to reading memory (MEM
            command), the multimeter automatically reconstructs the samples producing
            a composite waveform. When the samples are sent to the output buffer, the
            controller must use an algorithm to reconstruct the composite waveform.
            parameters for this algorithm are provided by the SSPARM? command.\n
            - The effective_interval between samples and the total number of samples taken
            are specified by the SWEEP command. (You cannot use the NRDGS command
            for sub-sampling.) In sub-sampling, the multimeter will use as many periods of
            the input signal as necessary to achieve the specified effective_interval. The
            minimum effective_interval for sub-sampling is 10 nanoseconds.\n
            
        Returns:
            bool: status
        """
        if max_input >= 0 and max_input <= 1E3:
            return self.__write_data(f'SSDC {max_input}')
        else:
            return False