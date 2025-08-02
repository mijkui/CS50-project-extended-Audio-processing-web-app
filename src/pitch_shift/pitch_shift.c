#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

// Structure to hold WAV header information
typedef struct {
    uint8_t riff[4];           // "RIFF"
    uint32_t file_size;        // File size - 8
    uint8_t wave[4];           // "WAVE"
    uint8_t fmt[4];            // "fmt "
    uint32_t fmt_size;         // Format chunk size (16 for PCM)
    uint16_t audio_format;     // Audio format (1 for PCM)
    uint16_t num_channels;     // Number of channels
    uint32_t sample_rate;      // Sample rate
    uint32_t byte_rate;        // Byte rate
    uint16_t block_align;      // Block align
    uint16_t bits_per_sample;  // Bits per sample
    uint8_t data[4];           // "data"
    uint32_t data_size;        // Data chunk size
} WAVHeader;

// Simple linear interpolation for resampling
int16_t interpolate_sample(int16_t *samples, int index, float fraction) {
    if (index < 0) return 0;
    
    int16_t sample1 = samples[index];
    int16_t sample2 = (index + 1 < 0) ? 0 : samples[index + 1];
    
    return (int16_t)(sample1 + (sample2 - sample1) * fraction);
}

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./pitch_shift input.wav output.wav factor\n");
        printf("Example: ./pitch_shift input.wav output.wav 2.0 (doubles pitch)\n");
        printf("         ./pitch_shift input.wav output.wav 0.5 (halves pitch)\n");
        return 1;
    }

    // Open input file
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open input file.\n");
        return 1;
    }

    // Open output file
    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open output file.\n");
        fclose(input);
        return 1;
    }

    float factor = atof(argv[3]);
    if (factor <= 0)
    {
        printf("Factor must be positive.\n");
        fclose(input);
        fclose(output);
        return 1;
    }

    // Read the header
    uint8_t header[HEADER_SIZE];
    if (fread(header, HEADER_SIZE, 1, input) != 1)
    {
        printf("Could not read WAV header.\n");
        fclose(input);
        fclose(output);
        return 1;
    }

    // Parse header
    WAVHeader *wav_header = (WAVHeader *)header;
    
    // Check if this is a valid WAV file
    if (memcmp(wav_header->riff, "RIFF", 4) != 0 || 
        memcmp(wav_header->wave, "WAVE", 4) != 0)
    {
        printf("Not a valid WAV file.\n");
        fclose(input);
        fclose(output);
        return 1;
    }

    // Calculate number of samples
    int num_samples = wav_header->data_size / (wav_header->bits_per_sample / 8);
    int num_channels = wav_header->num_channels;
    int samples_per_channel = num_samples / num_channels;

    printf("Processing %d samples per channel...\n", samples_per_channel);

    // Allocate memory for samples
    int16_t *input_samples = malloc(num_samples * sizeof(int16_t));
    int16_t *output_samples = malloc(num_samples * sizeof(int16_t));
    
    if (input_samples == NULL || output_samples == NULL)
    {
        printf("Memory allocation failed.\n");
        free(input_samples);
        free(output_samples);
        fclose(input);
        fclose(output);
        return 1;
    }

    // Read all samples
    if (fread(input_samples, sizeof(int16_t), num_samples, input) != num_samples)
    {
        printf("Could not read audio data.\n");
        free(input_samples);
        free(output_samples);
        fclose(input);
        fclose(output);
        return 1;
    }

    // Process each channel separately
    for (int ch = 0; ch < num_channels; ch++)
    {
        // Extract samples for this channel
        int16_t *channel_samples = malloc(samples_per_channel * sizeof(int16_t));
        for (int i = 0; i < samples_per_channel; i++)
        {
            channel_samples[i] = input_samples[i * num_channels + ch];
        }

        // Apply pitch shifting using simple resampling
        for (int i = 0; i < samples_per_channel; i++)
        {
            float source_index = i / factor;
            int int_index = (int)source_index;
            float fraction = source_index - int_index;
            
            int16_t new_sample = interpolate_sample(channel_samples, int_index, fraction);
            output_samples[i * num_channels + ch] = new_sample;
        }

        free(channel_samples);
    }

    // Write header to output file
    fwrite(header, HEADER_SIZE, 1, output);

    // Write processed samples
    fwrite(output_samples, sizeof(int16_t), num_samples, output);

    // Clean up
    free(input_samples);
    free(output_samples);
    fclose(input);
    fclose(output);

    printf("Pitch shifting complete!\n");
    printf("Pitch factor: %.2f\n", factor);
    printf("Output file: %s\n", argv[2]);

    return 0;
} 