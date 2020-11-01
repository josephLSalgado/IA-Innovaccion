using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.CognitiveServices.Speech;
using Microsoft.CognitiveServices.Speech.Audio;

public class Program
{
    static async Task Main(string[] args)
    {
        // replace with your own subscription key 
        string subscriptionKey = "SubscriptionKey";
        string region = "ServiceRegion";
        var config = SpeechConfig.FromSubscription(subscriptionKey, region);

        // persist profileMapping if you want to store a record of who the profile is
        var profileMapping = new Dictionary<string, string>();
        await VerificationEnroll(config, profileMapping);

        Console.ReadLine();
    }

    public static async Task VerificationEnroll(SpeechConfig config, Dictionary<string, string> profileMapping)
    {
        using (var client = new VoiceProfileClient(config))
        //using (var profile = await client.CreateProfileAsync(VoiceProfileType.TextDependentVerification, "en-us"))
        // independiente de texto
        using (var profile = await client.CreateProfileAsync(VoiceProfileType.TextIndependentVerification, "en-us"))
        {
            using (var audioInput = AudioConfig.FromDefaultMicrophoneInput())
            {
                Console.WriteLine($"Enrolling profile id {profile.Id}.");
                // give the profile a human-readable display name
                profileMapping.Add(profile.Id, "Joseph");

                VoiceProfileEnrollmentResult result = null;
                /*
                while (result is null || result.RemainingEnrollmentsCount > 0)
                {
                    Console.WriteLine("Speak the passphrase, \"My voice is my passport, verify me.\"");
                    result = await client.EnrollProfileAsync(profile, audioInput);
                    Console.WriteLine($"Remaining enrollments needed: {result.RemainingEnrollmentsCount}");
                    Console.WriteLine("");
                }*/

                // independiente de texto
                while (result is null || result.RemainingEnrollmentsSpeechLength > TimeSpan.Zero)
                {
                    Console.WriteLine("Continue speaking to add to the profile enrollment sample.");
                    result = await client.EnrollProfileAsync(profile, audioInput);
                    Console.WriteLine($"Remaining enrollment audio time needed: {result.RemainingEnrollmentsSpeechLength}");
                    Console.WriteLine("");
                }

                if (result.Reason == ResultReason.EnrolledVoiceProfile)
                {
                    await SpeakerVerify(config, profile, profileMapping);
                }
                else if (result.Reason == ResultReason.Canceled)
                {
                    var cancellation = VoiceProfileEnrollmentCancellationDetails.FromResult(result);
                    Console.WriteLine($"CANCELED {profile.Id}: ErrorCode={cancellation.ErrorCode} ErrorDetails={cancellation.ErrorDetails}");
                }
            }
        }
    }

    public static async Task SpeakerVerify(SpeechConfig config, VoiceProfile profile, Dictionary<string, string> profileMapping)
    {
        var speakerRecognizer = new SpeakerRecognizer(config, AudioConfig.FromDefaultMicrophoneInput());
        var model = SpeakerVerificationModel.FromProfile(profile);

        Console.WriteLine("Speak the passphrase to verify: \"My voice is my passport, please verify me.\"");
        var result = await speakerRecognizer.RecognizeOnceAsync(model);
        Console.WriteLine($"Verified voice profile for speaker {profileMapping[result.ProfileId]}, score is {result.Score}");
    }    
}
