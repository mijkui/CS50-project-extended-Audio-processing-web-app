#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
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

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./frequency input.wav output.wav factor\n");
        printf("Example: ./frequency input.wav output.wav 2.0 (doubles frequency)\n");
        printf("         ./frequency input.wav output.wav 0.5 (halves frequency)\n");
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

    // Read the entire header
    uint8_t header[HEADER_SIZE];
    if (fread(header, HEADER_SIZE, 1, input) != 1)
    {
        printf("Could not read WAV header.\n");
        fclose(input);
        fclose(output);
        return 1;
    }

    // Parse header to get current sample rate
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

    // Calculate new sample rate
    uint32_t original_sample_rate = wav_header->sample_rate;
    uint32_t new_sample_rate = (uint32_t)(original_sample_rate * factor);
    
    // Update header with new sample rate
    wav_header->sample_rate = new_sample_rate;
    
    // Recalculate byte rate (sample_rate * num_channels * bits_per_sample / 8)
    wav_header->byte_rate = new_sample_rate * wav_header->num_channels * wav_header->bits_per_sample / 8;
    
    // Recalculate file size
    wav_header->file_size = wav_header->data_size + 36; // 36 = header size - 8

    // Write modified header to output file
    fwrite(header, HEADER_SIZE, 1, output);

    // Copy all audio data unchanged
    uint8_t buffer[1024];
    size_t bytes_read;
    while ((bytes_read = fread(buffer, 1, sizeof(buffer), input)) > 0)
    {
        fwrite(buffer, 1, bytes_read, output);
    }

    // Close files
    fclose(input);
    fclose(output);

    printf("Frequency change complete!\n");
    printf("Original sample rate: %u Hz\n", original_sample_rate);
    printf("New sample rate: %u Hz\n", new_sample_rate);
    printf("Frequency factor: %.2f\n", factor);
    printf("Output file: %s\n", argv[2]);

    return 0;
} 