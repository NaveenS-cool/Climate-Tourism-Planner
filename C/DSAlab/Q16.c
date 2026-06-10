#include <stdio.h>
#include <stdlib.h>

#define MAX 100

// Structure to store coordinates and distance
typedef struct {
    int x, y, dist;
} Node;

// Queue implementation
typedef struct {
    Node data[MAX * MAX];
    int front, rear;
} Queue;

void initQueue(Queue *q) {
    q->front = q->rear = -1;
}

int isEmpty(Queue *q) {
    return q->front == -1;
}

void enqueue(Queue *q, Node val) {
    if (q->rear == MAX * MAX - 1) return;
    if (q->front == -1) q->front = 0;
    q->rear++;
    q->data[q->rear] = val;
}

Node dequeue(Queue *q) {
    Node val = q->data[q->front];
    if (q->front == q->rear)
        q->front = q->rear = -1;
    else
        q->front++;
    return val;
}


int dx[] = {-1, 1, 0, 0};
int dy[] = {0, 0, -1, 1};


int isValid(int x, int y, int n, int m, int visited[MAX][MAX], int maze[MAX][MAX]) {
    return (x >= 0 && x < n && y >= 0 && y < m && !visited[x][y] && maze[x][y] == 0);
}


int findShortestPath(int maze[MAX][MAX], int n, int m, int sx, int sy, int ex, int ey) {
    int visited[MAX][MAX] = {0};
    int parentX[MAX][MAX], parentY[MAX][MAX]; // store parent coordinates
    Queue q;
    initQueue(&q);

    Node start = {sx, sy, 0};
    enqueue(&q, start);
    visited[sx][sy] = 1;
    parentX[sx][sy] = -1;
    parentY[sx][sy] = -1;

    while (!isEmpty(&q)) {
        Node curr = dequeue(&q);

        // Reached charging point
        if (curr.x == ex && curr.y == ey) {

            printf("Minimum distance (battery units): %d\n", curr.dist);

            // Backtrack to print path
            int pathX[MAX * MAX], pathY[MAX * MAX];
            int len = 0, cx = ex, cy = ey;

            while (cx != -1 && cy != -1) {
                pathX[len] = cx;
                pathY[len] = cy;
                int px = parentX[cx][cy];
                int py = parentY[cx][cy];
                cx = px; cy = py;
                len++;
            }

            printf("\nPath followed (from start to charger):\n");
            for (int i = len - 1; i >= 0; i--) {
                printf("(%d, %d)", pathX[i], pathY[i]);
                if (i != 0) printf(" -> ");
            }
            printf("\n");
            return curr.dist;
        }

        // Explore all directions
        for (int i = 0; i < 4; i++) {
            int nx = curr.x + dx[i];
            int ny = curr.y + dy[i];

            if (isValid(nx, ny, n, m, visited, maze)) {
                visited[nx][ny] = 1;
                parentX[nx][ny] = curr.x;
                parentY[nx][ny] = curr.y;
                Node next = {nx, ny, curr.dist + 1};
                enqueue(&q, next);
            }
        }
    }

    printf("No path exists for DOTSLASH to reach the charger!\n");
    return -1;
}

int main() {
    int n, m;
    printf("Enter maze size (rows cols): ");
    scanf("%d %d", &n, &m);

    int maze[MAX][MAX];
    printf("Enter the maze (0 = path, 1 = wall):\n");
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            scanf("%d", &maze[i][j]);

    int sx, sy, ex, ey;
    printf("Enter robot start position (row col): ");
    scanf("%d %d", &sx, &sy);
    printf("Enter charging point position (row col): ");
    scanf("%d %d", &ex, &ey);

    findShortestPath(maze, n, m, sx, sy, ex, ey);
    return 0;
}