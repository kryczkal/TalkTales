classdef Comparer_exported < matlab.apps.AppBase

    % Properties that correspond to app components
    properties (Access = public)
        UIFigure                    matlab.ui.Figure
        Audio2manualEditField       matlab.ui.control.EditField
        Audio2manualEditFieldLabel  matlab.ui.control.Label
        Audio1manualEditField       matlab.ui.control.EditField
        Audio1manualEditFieldLabel  matlab.ui.control.Label
        Audio2ListBox               matlab.ui.control.ListBox
        Audio2ListBoxLabel          matlab.ui.control.Label
        Audio1ListBox               matlab.ui.control.ListBox
        Audio1ListBoxLabel          matlab.ui.control.Label
        Label2                      matlab.ui.control.Label
        Label                       matlab.ui.control.Label
        UIAxes22                    matlab.ui.control.UIAxes
        UIAxes21                    matlab.ui.control.UIAxes
        UIAxes12                    matlab.ui.control.UIAxes
        UIAxes11                    matlab.ui.control.UIAxes
    end

    % Callbacks that handle component events
    methods (Access = private)

        % Clicked callback: Audio1ListBox
        function Audio1ListBoxClicked(app, event)
            item = event.InteractionInformation.Item;
            
        end

        % Value changed function: Audio1ListBox
        function Audio1ListBoxValueChanged(app, event)

            value = app.Audio1ListBox.Value;
            [y, Fs] = audioread(value);
            [~, name, ext] = fileparts(value);
            
            tmp = char(name);
            if(strcmp(tmp(1:2), '22'))
                f = 22050;
            end
            if(strcmp(tmp(1:2), '44'))
                f = 44100;
            end
            if(strcmp(tmp(1:2), '96'))
                f = 96000;
            end
            t = (0:length(y)-1)/f;
            plot(app.UIAxes11, t, y);

            
            ttl = replace(name, "_", "-");
            app.Label.Text = ttl;
            drawnow;

            [S,F,T] = pspectrum(transpose(y),f,'spectrogram', 'FrequencyLimits',[0 f/2],'MinThreshold',-110);
 
            imagesc(app.UIAxes12, T, flipud(F), rot90(log(abs(S')))); %plot the log spectrum
             
            set(app.UIAxes12,'YDir', 'normal'); % flip the Y Axis
    

        end

        % Value changed function: Audio2ListBox
        function Audio2ListBoxValueChanged(app, event)
            value = app.Audio2ListBox.Value;
            [y, ~] = audioread(value);
            [~, name, ~] = fileparts(value);
            tmp = char(name);
            if(strcmp(tmp(1:2), '22'))
                f = 22050;
            end
            if(strcmp(tmp(1:2), '44'))
                f = 44100;
            end
            if(strcmp(tmp(1:2), '96'))
                f = 96000;
            end
            t = (0:length(y)-1)/f;
            plot(app.UIAxes21, t, y);

            
            ttl = replace(name, "_", "-");
            app.Label.Text = ttl;
            drawnow;
            [S,F,T] = pspectrum(transpose(y),f,'spectrogram', 'FrequencyLimits',[0 f/2],'MinThreshold',-110);
 
            imagesc(app.UIAxes22, T, flipud(F), rot90(log(abs(S'))));
             
            set(app.UIAxes22,'YDir', 'normal'); 



        end

        % Value changed function: Audio1manualEditField
        function Audio1manualEditFieldValueChanged(app, event)
            value = app.Audio1manualEditField.Value;
            value = strcat("../../data/", value);
            [y, Fs] = audioread(value);
            [~, name, ext] = fileparts(value);
            
            tmp = char(name);
            if(strcmp(tmp(1:2), '22'))
                f = 22050;
            end
            if(strcmp(tmp(1:2), '44'))
                f = 44100;
            end
            if(strcmp(tmp(1:2), '96'))
                f = 96000;
            end
            t = (0:length(y)-1)/f;
            plot(app.UIAxes11, t, y);

            
            ttl = replace(name, "_", "-");
            app.Label.Text = ttl;
            drawnow;

            [S,F,T] = pspectrum(transpose(y),f,'spectrogram', 'FrequencyLimits',[0 f/2],'MinThreshold',-110);
 
            imagesc(app.UIAxes12, T, flipud(F), rot90(log(abs(S')))); %plot the log spectrum
             
            set(app.UIAxes12,'YDir', 'normal'); % flip the Y Axis
        end

        % Value changed function: Audio2manualEditField
        function Audio2manualEditFieldValueChanged(app, event)
            value = app.Audio2manualEditField.Value;
            value = strcat("../../data/", value);
            [y, Fs] = audioread(value);
            [~, name, ext] = fileparts(value);
            
            tmp = char(name);
            if(strcmp(tmp(1:2), '22'))
                f = 22050;
            end
            if(strcmp(tmp(1:2), '44'))
                f = 44100;
            end
            if(strcmp(tmp(1:2), '96'))
                f = 96000;
            end
            t = (0:length(y)-1)/f;
            plot(app.UIAxes21, t, y);

            
            ttl = replace(name, "_", "-");
            app.Label.Text = ttl;
            drawnow;

            [S,F,T] = pspectrum(transpose(y),f,'spectrogram', 'FrequencyLimits',[0 f/2],'MinThreshold',-110);
 
            imagesc(app.UIAxes22, T, flipud(F), rot90(log(abs(S')))); %plot the log spectrum
             
            set(app.UIAxes22,'YDir', 'normal'); % flip the Y Axis
        end
    end

    % Component initialization
    methods (Access = private)

        % Create UIFigure and components
        function createComponents(app)

            % Create UIFigure and hide until all components are created
            app.UIFigure = uifigure('Visible', 'off');
            app.UIFigure.Position = [100 100 1179 782];
            app.UIFigure.Name = 'MATLAB App';

            % Create UIAxes11
            app.UIAxes11 = uiaxes(app.UIFigure);
            title(app.UIAxes11, 'Wave')
            xlabel(app.UIAxes11, 'time')
            ylabel(app.UIAxes11, 'y[n]')
            zlabel(app.UIAxes11, 'Z')
            app.UIAxes11.YLim = [-1 1];
            app.UIAxes11.Position = [69 527 509 185];

            % Create UIAxes12
            app.UIAxes12 = uiaxes(app.UIFigure);
            title(app.UIAxes12, 'Spectogram')
            xlabel(app.UIAxes12, 'time')
            ylabel(app.UIAxes12, 'frequency')
            app.UIAxes12.Position = [640 527 476 185];

            % Create UIAxes21
            app.UIAxes21 = uiaxes(app.UIFigure);
            title(app.UIAxes21, 'Wave')
            xlabel(app.UIAxes21, 'X')
            ylabel(app.UIAxes21, 'Y')
            zlabel(app.UIAxes21, 'Z')
            app.UIAxes21.Position = [69 298 509 187];

            % Create UIAxes22
            app.UIAxes22 = uiaxes(app.UIFigure);
            title(app.UIAxes22, 'Spectogram')
            xlabel(app.UIAxes22, 'time')
            ylabel(app.UIAxes22, 'frequency')
            zlabel(app.UIAxes22, 'Z')
            app.UIAxes22.Position = [640 298 476 197];

            % Create Label
            app.Label = uilabel(app.UIFigure);
            app.Label.HorizontalAlignment = 'center';
            app.Label.Position = [374 732 479 22];

            % Create Label2
            app.Label2 = uilabel(app.UIFigure);
            app.Label2.HorizontalAlignment = 'center';
            app.Label2.Position = [374 494 479 22];
            app.Label2.Text = 'Label2';

            % Create Audio1ListBoxLabel
            app.Audio1ListBoxLabel = uilabel(app.UIFigure);
            app.Audio1ListBoxLabel.HorizontalAlignment = 'right';
            app.Audio1ListBoxLabel.Position = [42 209 42 22];
            app.Audio1ListBoxLabel.Text = 'Audio1';

            % Create Audio1ListBox
            app.Audio1ListBox = uilistbox(app.UIFigure);
            app.Audio1ListBox.Items = {'96_park_sofia_laptop.wav', '96_parking_wojtek_samson.wav', '44_parking_sofia_samson.wav', '44_zlote_sofiia_rode.wav', '22_zlote_sofiia_rode.wav', '22_biblioteka_tomasz_rode.wav', '96_parking_michal_samson.wav', '44_dworzec_wojtek_samson.wav', '96_dworzec_michal_samson.wav', '44_zlote_szum_rode.wav', '96_zlote_szum_rode.wav', '96_dworzec_szum_rode.wav', '96_dworzec_wojtek_samson.wav', '44_park_sofia_laptop.wav', '96_metro_sofia_laptop.wav', '22_parking_michal_samson.wav', '44_dworzec_sofia_samson.wav', '22_pokoj_sofia_samson.wav', '22_biblioteka_szum_rode.wav', '22_dworzec_sofia_samson.wav', '96_zlote_mateusz_rode.wav', '96_park_wojtek_laptop.wav', '44_parking_michal_samson.wav', '44_parking_wojtek_samson.wav', '22_gmach_szum_rode.wav', '96_biblioteka_tomasz_rode.wav', '96_dworzec_mateusz_rode.wav', '96_gmach_szum_rode.wav', '22_gmach_mateusz_rode.wav', '22_gmach_sofiia_rode.wav', '44_dworzec_szum_rode.wav', '44_biblioteka_sofiia_rode.wav', '96_biblioteka_szum_rode.wav', '22_dworzec_michal_samson.wav', '44_biblioteka_szum_rode.wav', '22_metro_sofia_laptop.wav', '44_dworzec_michal_samson.wav', '44_gmach_szum_rode.wav', '22_park_michal_laptop.wav', '44_zlote_mateusz_rode.wav', '44_gmach_sofiia_rode.wav', '44_park_michal_laptop.wav', '44_pokoj_michal_samson.wav', '96_biblioteka_sofiia_rode.wav', '96_dworzec_tomasz_rode.wav', '96_metro_michal_laptop.wav', '96_zlote_tomasz_rode.wav', '96_gmach_mateusz_rode.wav', '22_parking_wojtek_samson.wav', '22_gmach_tomasz_rode.wav', '44_metro_wojtek_laptop.wav', '22_pokoj_wojtek_samson.wav', '44_metro_michal_laptop.wav', '44_metro_sofia_laptop.wav', '96_biblioteka_mateusz_rode.wav', '44_park_wojtek_laptop.wav', '96_pokoj_sofia_samson.wav', '44_dworzec_tomasz_rode.wav', '96_gmach_sofiia_rode.wav', '44_zlote_tomasz_rode.wav', '44_dworzec_mateusz_rode.wav', '22_parking_sofia_samson.wav', '96_metro_wojtek_laptop.wav', '44_biblioteka_mateusz_rode.wav', '96_gmach_tomasz_rode.wav', '96_parking_sofia_samson.wav', '22_zlote_szum_rode.wav', '44_biblioteka_tomasz_rode.wav', '22_park_sofia_laptop.wav', '22_dworzec_wojtek_samson.wav', '96_pokoj_michal_samson.wav', '96_park_michal_laptop.wav', '22_zlote_tomasz_rode.wav', '96_zlote_sofiia_rode.wav', '44_pokoj_sofia_samson.wav', '44_pokoj_wojtek_samson.wav', '44_gmach_tomasz_rode.wav', '22_pokoj_michal_samson.wav', '96_dworzec_sofia_samson.wav', '22_metro_wojtek_laptop.wav', '44_gmach_mateusz_rode.wav', '22_biblioteka_sofiia_rode.wav', '22_metro_michal_laptop.wav', '96_pokoj_wojtek_samson.wav', '22_biblioteka_mateusz_rode.wav', '22_zlote_mateusz_rode.wav', '22_park_wojtek_laptop.wav'};
            app.Audio1ListBox.ItemsData = {'../../data/96_park_sofia_laptop.wav', '../../data/96_parking_wojtek_samson.wav', '../../data/44_parking_sofia_samson.wav', '../../data/44_zlote_sofiia_rode.wav', '../../data/22_zlote_sofiia_rode.wav', '../../data/22_biblioteka_tomasz_rode.wav', '../../data/96_parking_michal_samson.wav', '../../data/44_dworzec_wojtek_samson.wav', '../../data/96_dworzec_michal_samson.wav', '../../data/44_zlote_szum_rode.wav', '../../data/96_zlote_szum_rode.wav', '../../data/96_dworzec_szum_rode.wav', '../../data/96_dworzec_wojtek_samson.wav', '../../data/44_park_sofia_laptop.wav', '../../data/96_metro_sofia_laptop.wav', '../../data/22_parking_michal_samson.wav', '../../data/44_dworzec_sofia_samson.wav', '../../data/22_pokoj_sofia_samson.wav', '../../data/22_biblioteka_szum_rode.wav', '../../data/22_dworzec_sofia_samson.wav', '../../data/96_zlote_mateusz_rode.wav', '../../data/96_park_wojtek_laptop.wav', '../../data/44_parking_michal_samson.wav', '../../data/44_parking_wojtek_samson.wav', '../../data/22_gmach_szum_rode.wav', '../../data/96_biblioteka_tomasz_rode.wav', '../../data/96_dworzec_mateusz_rode.wav', '../../data/96_gmach_szum_rode.wav', '../../data/22_gmach_mateusz_rode.wav', '../../data/22_gmach_sofiia_rode.wav', '../../data/44_dworzec_szum_rode.wav', '../../data/44_biblioteka_sofiia_rode.wav', '../../data/96_biblioteka_szum_rode.wav', '../../data/22_dworzec_michal_samson.wav', '../../data/44_biblioteka_szum_rode.wav', '../../data/22_metro_sofia_laptop.wav', '../../data/44_dworzec_michal_samson.wav', '../../data/44_gmach_szum_rode.wav', '../../data/22_park_michal_laptop.wav', '../../data/44_zlote_mateusz_rode.wav', '../../data/44_gmach_sofiia_rode.wav', '../../data/44_park_michal_laptop.wav', '../../data/44_pokoj_michal_samson.wav', '../../data/96_biblioteka_sofiia_rode.wav', '../../data/96_dworzec_tomasz_rode.wav', '../../data/96_metro_michal_laptop.wav', '../../data/96_zlote_tomasz_rode.wav', '../../data/96_gmach_mateusz_rode.wav', '../../data/22_parking_wojtek_samson.wav', '../../data/22_gmach_tomasz_rode.wav', '../../data/44_metro_wojtek_laptop.wav', '../../data/22_pokoj_wojtek_samson.wav', '../../data/44_metro_michal_laptop.wav', '../../data/44_metro_sofia_laptop.wav', '../../data/96_biblioteka_mateusz_rode.wav', '../../data/44_park_wojtek_laptop.wav', '../../data/96_pokoj_sofia_samson.wav', '../../data/44_dworzec_tomasz_rode.wav', '../../data/96_gmach_sofiia_rode.wav', '../../data/44_zlote_tomasz_rode.wav', '../../data/44_dworzec_mateusz_rode.wav', '../../data/22_parking_sofia_samson.wav', '../../data/96_metro_wojtek_laptop.wav', '../../data/44_biblioteka_mateusz_rode.wav', '../../data/96_gmach_tomasz_rode.wav', '../../data/96_parking_sofia_samson.wav', '../../data/22_zlote_szum_rode.wav', '../../data/44_biblioteka_tomasz_rode.wav', '../../data/22_park_sofia_laptop.wav', '../../data/22_dworzec_wojtek_samson.wav', '../../data/96_pokoj_michal_samson.wav', '../../data/96_park_michal_laptop.wav', '../../data/22_zlote_tomasz_rode.wav', '../../data/96_zlote_sofiia_rode.wav', '../../data/44_pokoj_sofia_samson.wav', '../../data/44_pokoj_wojtek_samson.wav', '../../data/44_gmach_tomasz_rode.wav', '../../data/22_pokoj_michal_samson.wav', '../../data/96_dworzec_sofia_samson.wav', '../../data/22_metro_wojtek_laptop.wav', '../../data/44_gmach_mateusz_rode.wav', '../../data/22_biblioteka_sofiia_rode.wav', '../../data/22_metro_michal_laptop.wav', '../../data/96_pokoj_wojtek_samson.wav', '../../data/22_biblioteka_mateusz_rode.wav', '../../data/22_zlote_mateusz_rode.wav', '../../data/22_park_wojtek_laptop.wav'};
            app.Audio1ListBox.ValueChangedFcn = createCallbackFcn(app, @Audio1ListBoxValueChanged, true);
            app.Audio1ListBox.ClickedFcn = createCallbackFcn(app, @Audio1ListBoxClicked, true);
            app.Audio1ListBox.Position = [99 41 395 192];
            app.Audio1ListBox.Value = '../../data/96_park_sofia_laptop.wav';

            % Create Audio2ListBoxLabel
            app.Audio2ListBoxLabel = uilabel(app.UIFigure);
            app.Audio2ListBoxLabel.HorizontalAlignment = 'right';
            app.Audio2ListBoxLabel.Position = [640 207 42 22];
            app.Audio2ListBoxLabel.Text = 'Audio2';

            % Create Audio2ListBox
            app.Audio2ListBox = uilistbox(app.UIFigure);
            app.Audio2ListBox.Items = {'96_park_sofia_laptop.wav', '96_parking_wojtek_samson.wav', '44_parking_sofia_samson.wav', '44_zlote_sofiia_rode.wav', '22_zlote_sofiia_rode.wav', '22_biblioteka_tomasz_rode.wav', '96_parking_michal_samson.wav', '44_dworzec_wojtek_samson.wav', '96_dworzec_michal_samson.wav', '44_zlote_szum_rode.wav', '96_zlote_szum_rode.wav', '96_dworzec_szum_rode.wav', '96_dworzec_wojtek_samson.wav', '44_park_sofia_laptop.wav', '96_metro_sofia_laptop.wav', '22_parking_michal_samson.wav', '44_dworzec_sofia_samson.wav', '22_pokoj_sofia_samson.wav', '22_biblioteka_szum_rode.wav', '22_dworzec_sofia_samson.wav', '96_zlote_mateusz_rode.wav', '96_park_wojtek_laptop.wav', '44_parking_michal_samson.wav', '44_parking_wojtek_samson.wav', '22_gmach_szum_rode.wav', '96_biblioteka_tomasz_rode.wav', '96_dworzec_mateusz_rode.wav', '96_gmach_szum_rode.wav', '22_gmach_mateusz_rode.wav', '22_gmach_sofiia_rode.wav', '44_dworzec_szum_rode.wav', '44_biblioteka_sofiia_rode.wav', '96_biblioteka_szum_rode.wav', '22_dworzec_michal_samson.wav', '44_biblioteka_szum_rode.wav', '22_metro_sofia_laptop.wav', '44_dworzec_michal_samson.wav', '44_gmach_szum_rode.wav', '22_park_michal_laptop.wav', '44_zlote_mateusz_rode.wav', '44_gmach_sofiia_rode.wav', '44_park_michal_laptop.wav', '44_pokoj_michal_samson.wav', '96_biblioteka_sofiia_rode.wav', '96_dworzec_tomasz_rode.wav', '96_metro_michal_laptop.wav', '96_zlote_tomasz_rode.wav', '96_gmach_mateusz_rode.wav', '22_parking_wojtek_samson.wav', '22_gmach_tomasz_rode.wav', '44_metro_wojtek_laptop.wav', '22_pokoj_wojtek_samson.wav', '44_metro_michal_laptop.wav', '44_metro_sofia_laptop.wav', '96_biblioteka_mateusz_rode.wav', '44_park_wojtek_laptop.wav', '96_pokoj_sofia_samson.wav', '44_dworzec_tomasz_rode.wav', '96_gmach_sofiia_rode.wav', '44_zlote_tomasz_rode.wav', '44_dworzec_mateusz_rode.wav', '22_parking_sofia_samson.wav', '96_metro_wojtek_laptop.wav', '44_biblioteka_mateusz_rode.wav', '96_gmach_tomasz_rode.wav', '96_parking_sofia_samson.wav', '22_zlote_szum_rode.wav', '44_biblioteka_tomasz_rode.wav', '22_park_sofia_laptop.wav', '22_dworzec_wojtek_samson.wav', '96_pokoj_michal_samson.wav', '96_park_michal_laptop.wav', '22_zlote_tomasz_rode.wav', '96_zlote_sofiia_rode.wav', '44_pokoj_sofia_samson.wav', '44_pokoj_wojtek_samson.wav', '44_gmach_tomasz_rode.wav', '22_pokoj_michal_samson.wav', '96_dworzec_sofia_samson.wav', '22_metro_wojtek_laptop.wav', '44_gmach_mateusz_rode.wav', '22_biblioteka_sofiia_rode.wav', '22_metro_michal_laptop.wav', '96_pokoj_wojtek_samson.wav', '22_biblioteka_mateusz_rode.wav', '22_zlote_mateusz_rode.wav', '22_park_wojtek_laptop.wav'};
            app.Audio2ListBox.ItemsData = {'../../data/96_park_sofia_laptop.wav', '../../data/96_parking_wojtek_samson.wav', '../../data/44_parking_sofia_samson.wav', '../../data/44_zlote_sofiia_rode.wav', '../../data/22_zlote_sofiia_rode.wav', '../../data/22_biblioteka_tomasz_rode.wav', '../../data/96_parking_michal_samson.wav', '../../data/44_dworzec_wojtek_samson.wav', '../../data/96_dworzec_michal_samson.wav', '../../data/44_zlote_szum_rode.wav', '../../data/96_zlote_szum_rode.wav', '../../data/96_dworzec_szum_rode.wav', '../../data/96_dworzec_wojtek_samson.wav', '../../data/44_park_sofia_laptop.wav', '../../data/96_metro_sofia_laptop.wav', '../../data/22_parking_michal_samson.wav', '../../data/44_dworzec_sofia_samson.wav', '../../data/22_pokoj_sofia_samson.wav', '../../data/22_biblioteka_szum_rode.wav', '../../data/22_dworzec_sofia_samson.wav', '../../data/96_zlote_mateusz_rode.wav', '../../data/96_park_wojtek_laptop.wav', '../../data/44_parking_michal_samson.wav', '../../data/44_parking_wojtek_samson.wav', '../../data/22_gmach_szum_rode.wav', '../../data/96_biblioteka_tomasz_rode.wav', '../../data/96_dworzec_mateusz_rode.wav', '../../data/96_gmach_szum_rode.wav', '../../data/22_gmach_mateusz_rode.wav', '../../data/22_gmach_sofiia_rode.wav', '../../data/44_dworzec_szum_rode.wav', '../../data/44_biblioteka_sofiia_rode.wav', '../../data/96_biblioteka_szum_rode.wav', '../../data/22_dworzec_michal_samson.wav', '../../data/44_biblioteka_szum_rode.wav', '../../data/22_metro_sofia_laptop.wav', '../../data/44_dworzec_michal_samson.wav', '../../data/44_gmach_szum_rode.wav', '../../data/22_park_michal_laptop.wav', '../../data/44_zlote_mateusz_rode.wav', '../../data/44_gmach_sofiia_rode.wav', '../../data/44_park_michal_laptop.wav', '../../data/44_pokoj_michal_samson.wav', '../../data/96_biblioteka_sofiia_rode.wav', '../../data/96_dworzec_tomasz_rode.wav', '../../data/96_metro_michal_laptop.wav', '../../data/96_zlote_tomasz_rode.wav', '../../data/96_gmach_mateusz_rode.wav', '../../data/22_parking_wojtek_samson.wav', '../../data/22_gmach_tomasz_rode.wav', '../../data/44_metro_wojtek_laptop.wav', '../../data/22_pokoj_wojtek_samson.wav', '../../data/44_metro_michal_laptop.wav', '../../data/44_metro_sofia_laptop.wav', '../../data/96_biblioteka_mateusz_rode.wav', '../../data/44_park_wojtek_laptop.wav', '../../data/96_pokoj_sofia_samson.wav', '../../data/44_dworzec_tomasz_rode.wav', '../../data/96_gmach_sofiia_rode.wav', '../../data/44_zlote_tomasz_rode.wav', '../../data/44_dworzec_mateusz_rode.wav', '../../data/22_parking_sofia_samson.wav', '../../data/96_metro_wojtek_laptop.wav', '../../data/44_biblioteka_mateusz_rode.wav', '../../data/96_gmach_tomasz_rode.wav', '../../data/96_parking_sofia_samson.wav', '../../data/22_zlote_szum_rode.wav', '../../data/44_biblioteka_tomasz_rode.wav', '../../data/22_park_sofia_laptop.wav', '../../data/22_dworzec_wojtek_samson.wav', '../../data/96_pokoj_michal_samson.wav', '../../data/96_park_michal_laptop.wav', '../../data/22_zlote_tomasz_rode.wav', '../../data/96_zlote_sofiia_rode.wav', '../../data/44_pokoj_sofia_samson.wav', '../../data/44_pokoj_wojtek_samson.wav', '../../data/44_gmach_tomasz_rode.wav', '../../data/22_pokoj_michal_samson.wav', '../../data/96_dworzec_sofia_samson.wav', '../../data/22_metro_wojtek_laptop.wav', '../../data/44_gmach_mateusz_rode.wav', '../../data/22_biblioteka_sofiia_rode.wav', '../../data/22_metro_michal_laptop.wav', '../../data/96_pokoj_wojtek_samson.wav', '../../data/22_biblioteka_mateusz_rode.wav', '../../data/22_zlote_mateusz_rode.wav', '../../data/22_park_wojtek_laptop.wav'};
            app.Audio2ListBox.ValueChangedFcn = createCallbackFcn(app, @Audio2ListBoxValueChanged, true);
            app.Audio2ListBox.Position = [697 41 395 190];
            app.Audio2ListBox.Value = '../../data/96_park_sofia_laptop.wav';

            % Create Audio1manualEditFieldLabel
            app.Audio1manualEditFieldLabel = uilabel(app.UIFigure);
            app.Audio1manualEditFieldLabel.HorizontalAlignment = 'right';
            app.Audio1manualEditFieldLabel.Position = [69 247 85 22];
            app.Audio1manualEditFieldLabel.Text = 'Audio1 manual';

            % Create Audio1manualEditField
            app.Audio1manualEditField = uieditfield(app.UIFigure, 'text');
            app.Audio1manualEditField.ValueChangedFcn = createCallbackFcn(app, @Audio1manualEditFieldValueChanged, true);
            app.Audio1manualEditField.Position = [169 247 316 22];

            % Create Audio2manualEditFieldLabel
            app.Audio2manualEditFieldLabel = uilabel(app.UIFigure);
            app.Audio2manualEditFieldLabel.HorizontalAlignment = 'right';
            app.Audio2manualEditFieldLabel.Position = [674 247 85 22];
            app.Audio2manualEditFieldLabel.Text = 'Audio2 manual';

            % Create Audio2manualEditField
            app.Audio2manualEditField = uieditfield(app.UIFigure, 'text');
            app.Audio2manualEditField.ValueChangedFcn = createCallbackFcn(app, @Audio2manualEditFieldValueChanged, true);
            app.Audio2manualEditField.Position = [774 247 318 22];

            % Show the figure after all components are created
            app.UIFigure.Visible = 'on';
        end
    end

    % App creation and deletion
    methods (Access = public)

        % Construct app
        function app = Comparer_exported

            % Create UIFigure and components
            createComponents(app)

            % Register the app with App Designer
            registerApp(app, app.UIFigure)

            if nargout == 0
                clear app
            end
        end

        % Code that executes before app deletion
        function delete(app)

            % Delete UIFigure when app is deleted
            delete(app.UIFigure)
        end
    end
end