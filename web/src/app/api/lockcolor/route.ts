// https://developer.mozilla.org/docs/Web/API/ReadableStream#convert_async_iterator_to_stream

// Attempt at streaming back to the server
// This file should be ignored for now

export async function POST(request: Request) {
  console.log("inside lockcolor route again");
  try {
    const body = request.body;
    if (body) {
      const reader = body.getReader();
      const stream = new ReadableStream({
        start(controller) {
          // The following function handles each data chunk
          function push() {
            // "done" is a Boolean and value a "Uint8Array"
            void reader.read().then(({ done, value }) => {
              // If there is no more data to read
              if (done) {
                console.log("done", done);
                controller.close();
                return;
              }
              // Get the data and send it to the browser via the controller
              controller.enqueue(value);
              // Check chunks by logging to the console
              console.log(done, value);
              push();
            });
          }

          push();
        },
      });
      console.log("stream", stream);
      // for await (const chunk of stream) {
      //   console.log(chunk);
      // }
    }
    // Process the webhook payload
  } catch (error) {
    console.log(error);
    // @ts-expect-error non deterministic
    return new Response(`Webhook error: ${error.message}`, {
      status: 400,
    });
  }

  return new Response("Success!", {
    status: 200,
  });
}
